from math import e
import platform
import sys
import datetime
from datetime import time, datetime, date
import undetected_chromedriver as uc
from selenium import webdriver

def get_driver_path():
    # Directory
    system = platform.system()

    if system == "Windows":
        driver_path = r"D:\Programming\nc-studyform\chromedriver.exe"
    elif system == "Linux":
        driver_path = r'/home/Silver/insta-follow-tracker/chromedriver'
    
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

def fill_out_form(driver_path):
    print("Opening Browser...")
    options = uc.ChromeOptions()
    options.add_argument("-incognito")
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    # options.add_argument( "--user-data-dir=Default")
    # options.add_argument('--user-data-dir=./chrome_profile/')

    #option.add_argument("--headless")
    #option.add_argument("disable-gpu")

    # browser = uc.Chrome(executable_path=driver_path,options=options)
    Service = executable_path=driver_path
    browser = webdriver.Chrome(Service, options=options)

    browser.get("https://accounts.google.com/servicelogin")
    # WebDriverWait(driver, timeout=3).until(some_condition)





def main():
    driver_path = get_driver_path()
    period = get_period()
    print(driver_path, period)
    fill_out_form(driver_path)

if __name__ == "__main__":
    main()
