import datetime
import os
import platform
import time as time_wait
from datetime import date, datetime, time

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import credentials

# Credit, my saving grace https://medium.com/@hostapandey/google-login-with-selenium-solved-f58873af5de9


def get_driver_path():
    """Returns Driver path dependent on OS."""
    # Directory
    system = platform.system()

    if system == "Windows":
        driver_path = credentials.windows_driver_path
    elif system == "Linux":
        driver_path = credentials.linux_driver_path

    return driver_path


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x < end
    else:
        return start <= x or x < end


def get_period():
    # Get current time
    time_now = datetime.now().time()
    # Check if Thursday. If thursday, check for Thursday timetable times.
    if date.today().weekday() == 3:
        print("Thursday")
        if time_in_range(time(9,10,0), time(10,10,0), time_now):
            return 1
        elif time_in_range(time(10,10,0), time(11,5,0), time_now):
            return 2
        elif time_in_range(time(11,30,0), time(12,25,0), time_now):
            return 3
        elif time_in_range(time(12,25,0), time(13,20,0), time_now):
            return 4
        elif time_in_range(time(14,15,0), time(15,10,0), time_now):
            return 5

    else:
        if time_in_range(time(8,40,0), time(9,40,0), time_now):
            return 1
        elif time_in_range(time(9,40,0), time(10,40,0), time_now):
            return 2
        elif time_in_range(time(11,0,0), time(12,0,0), time_now):
            return 3
        elif time_in_range(time(12,0,0), time(13,0,0), time_now):
            return 4
        elif time_in_range(time(14,10,0), time(15,10,0), time_now):
            return 5


def login(browser, email, password):
    global headless
    browser.get("https://accounts.google.com/servicelogin")
    # browser.get('https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin')

    # Login username
    # username_field = browser.find_element(By.NAME, "identifier")
    if headless is False:
        username_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@id='identifierId']")))
    else:
        username_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[2]/div[2]/div[1]/form/div/div/div/div/div/input[1]")))

    username_field.clear()
    username_field.send_keys(email)

    # Click next button
    if headless is False:
        username_field.send_keys(u'\ue007')
    else:
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div[2]/div[2]/div[1]/form/div/div/input")
            )).click()

    time_wait.sleep(2)

    # password_field = browser.find_element(By.NAME, "password")
    if headless is False:
        password_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='password']")))
    else:
        password_field = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/form/span/div/div[2]/input")))

    password_field.clear()
    password_field.send_keys(password)

    # Click login button
    if headless is False:
        password_field.send_keys(u'\ue007')
    else:
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/form/span/div/input[2]")
            )).click()

    # Sleep, so google can authenticate before continuing
    time_wait.sleep(8)

def take_screenshot(browser):
    """
    Takes a selenium Screenshot
    
    Returns a string, path to screenshot.
    """
    current_date_with_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    system = platform.system()
    
    if system == "Linux":
        screenshot_folder = credentials.linux_screenshot_folder
    elif system == "Windows":
        screenshot_folder = credentials.windows_screenshot_folder
    
    # screenshot_path = f"{screenshot_folder}/{current_date_with_time}.png"
    screenshot_path = os.path.join(screenshot_folder, current_date_with_time + "a.png")

    # Take screenshot to folder.
    result = browser.save_screenshot(screenshot_path)
    print("Screenshot saved to", screenshot_path)

    # result = browser.find_element(By.TAG_NAME, "body").screenshot(screenshot_path)

    print(result)
    print("Result above")
    return screenshot_path

def fill_out_form(current_location):
    global headless

    driver_path = get_driver_path()
    current_period = get_period()

    print(driver_path, current_period)

    print("Opening Browser...")
    options = uc.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument('--no-sandbox')
    # options.add_argument('--user-data-dir=./chrome_profile/')

    if headless == True:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    Service = executable_path=driver_path
    # browser = uc.Chrome(Service ,options=options)
    browser = webdriver.Chrome(Service, options=options)
    browser.maximize_window()

    # Login to google
    login(browser, credentials.email, credentials.password)
    
    print("Authentication successful")

    # NOTE for testing purposes
    # current_period = 3

    # Create form link
    link = credentials.form_link
    link = link.replace("[period]", ("P" + str(current_period)))
    link = link.replace("[form_class]", str(credentials.form_class))
    link = link.replace("[location]", str(current_location))

    print("\n\n\n")
    print(link)
    print("\n\n\n")

    # Navigate to study form.
    browser.get(link)

    # Click continue on the "continue current draft" panel

    WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div/div[2]/div[3]/div[2]/a/span")
            )).click()

    time_wait.sleep(3)
    # Click "next"
    browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
    time_wait.sleep(2)

    # Take evidence screenshot
    screenshot_path = take_screenshot(browser)

    # Click "submit" 
    browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span/span').click()

    # Sleep to allow POST to go through
    time_wait.sleep(5)

    # End browser instance(s)
    browser.close()
    browser.quit()

    return screenshot_path


def main():
    global headless
    headless = False

    current_location = "thehall"
    fill_out_form(current_location)

if __name__ == "__main__":
    main()
