import datetime
import platform
import sys, os
import time as time_wait
from datetime import date, datetime, time
from math import e

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import credentials

# Credit, my saving grace https://medium.com/@hostapandey/google-login-with-selenium-solved-f58873af5de9


def get_driver_path():
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
    # browser.get("https://accounts.google.com/servicelogin")
    browser.get('https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    # WebDriverWait(driver, timeout=3).until(some_condition)

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
    if headless is False:
        password_field.send_keys(u'\ue007')
    else:
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/form/span/div/input[2]")
            )).click()

    time_wait.sleep(8)

def select_period(browser, current_period):
    # browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[1]').click()
    # browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[1]').click()
    # NOTE if headless, need to click the box TWICE
    open_box = WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[1]')
    ))
    open_box.click()
    # open_box.click()

    time_wait.sleep(1) # Sleep so box can open 
    
    # browser.save_screenshot("aa.png")

    # WebDriverWait(browser, 5).until(EC.element_to_be_clickable(
    #     (By.XPATH, f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[{current_period + 2}]')
    #     )).click()

    browser.find_element(By.XPATH, f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div[{current_period + 2}]').click()

def select_location_page1(browser):
    browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]').click()
    time_wait.sleep(0.5) # Sleep so box can open 
    browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[6]').click()


def fill_out_form(driver_path, current_period, current_location):
    global headless
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
    browser.implicitly_wait(10)
    browser.maximize_window()

    # Login to google
    login(browser, credentials.email, credentials.password)
    
    print("Authentication successful")
    # Navigate to study form.
    browser.get(credentials.form_link)

    # select current period, via dropdown menu
    select_period(browser, current_period)

    time_wait.sleep(1) # Sleep so box can open/close 


    # Enter form class
    form_class_field = browser.find_element(By.CLASS_NAME, "quantumWizTextinputPaperinputInput")
    form_class_field.click()
    form_class_field.send_keys(credentials.form_class)

    #! !!! NOTE IMPORTANT
    """
    Set period, then enter form class, then set location. 
    Cannot interact dropdown box then another dropdown box immediately after, must click elsewhere.
    Resolved by entering form class first.
    """

    # Set location as other in dropdown menu
    select_location_page1(browser)

    time_wait.sleep(1) # Sleep so box can open/close


    # Click "next"
    browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
    time_wait.sleep(2)

    # Enter location as hall (page 2)
    location_field = browser.find_element(By.CLASS_NAME, "quantumWizTextinputPaperinputInput")
    location_field.click()
    location_field.send_keys(current_location)

    # Take evidence screenshot
    current_date_with_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    system = platform.system()
    
    if system == "Linux":
        screenshot_folder = credentials.linux_screenshot_folder
    elif system == "Windows":
        screenshot_folder = credentials.windows_screenshot_folder
    
    # screenshot_path = f"{screenshot_folder}/{current_date_with_time}.png"
    screenshot_path = os.path.join(screenshot_folder, current_date_with_time + ".png")

    # Take screenshot to folder.
    result = browser.save_screenshot(screenshot_path)
    print("Screenshot saved to", screenshot_path)

    # result = browser.find_element(By.TAG_NAME, "body").screenshot(screenshot_path)



    print(result)
    print("Result above")

    # Click "submit" 
    browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span/span').click()
    
    time_wait.sleep(10)
    browser.close()
    return screenshot_path


def main():
    global headless
    headless = True
    driver_path = get_driver_path()
    current_period = get_period()
    print(driver_path, current_period)
    current_period = 3
    current_location = "dhall"
    fill_out_form(driver_path, current_period, current_location)

if __name__ == "__main__":
    main()
