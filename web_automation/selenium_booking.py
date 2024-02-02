# selenium_booking.py
# File is used for implementing web functionality to create a booking
# Right now in development

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from functions.web_functions import *
import os


def booking_flow(environment, email, password, ecoaccount, venue, category, report, fromdate, todate):
    # Website for driver, and required credentials
    website = set_web_environment(environment)

    # Unique path for each report download, dynamic directory allocation
    new_directory_path = os.path.join(os.getcwd(), report + venue + fromdate)
    # Create the directory if it doesn't exist
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
    chrome_options = Options()

    preferences = {
        "download.default_directory": new_directory_path,  # In a new dynamically made directory
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", preferences)

    # Set up the WebDriver, and initialize a timeout of 10 seconds
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1200, 900)
    wait = WebDriverWait(driver, 20)

    # Go to website
    driver.get(website)

    #############################################################
    ##  Initialize, Operation Auto: ACQUIRING THE REPORT!!!!!! ##
    #############################################################
    print("test")
    login_page(email, password, wait,  driver)
    godmode_page(wait, driver)
    ecoaccount_page(ecoaccount, wait, driver)
    venue_page(venue, wait, driver)
    select_report_page(category, report, wait, driver)
    filter_trick_page(wait, driver)
    update_url_date_page(fromdate, todate, driver)
    print("test2")
    df = acquire_report(new_directory_path, driver)

    return df
