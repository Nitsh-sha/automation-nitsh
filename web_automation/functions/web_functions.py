# web_functions.py
# Implements useful selenium functions to make an automated bookings
# TO-DO: Implement more web functions, ensure names are intuitive, and add more exception handling  when needed.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from  selenium.common.exceptions import TimeoutException, WebDriverException
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, ParseResult, ParseResultBytes
from report_generation.generate_report import wait_for_download_complete, click_download_button
import os
import pandas as pd


# Sets the url
def set_web_environment(environment):
    if environment == 'UAT':
        return "https://uat.urvenue.me"
    elif environment == 'LIVE':
        return "https://urvenue.me"
    elif environment == 'STAGING':
        return "https://staging.urvenue.me"
    else:
        raise Exception(f"Incorrect usage, available environments are UAT, LIVE, and STAGING")


# Enters username, presses enter
def username_page(email, wait, driver, new_directory_path):
    try:
        email_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[formcontrolname='email']")))
        email_input.send_keys(email + Keys.RETURN)
    except TimeoutException:
        print("Timeout error occurred when entering username")
        os.rmdir(new_directory_path)
        driver.quit()


#  Enters password, presses enter
def password_page(password, wait, driver, new_directory_path):
    try:
        password_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[formcontrolname='password']")))
        password_input.send_keys(password + Keys.RETURN)
    except TimeoutException:
        print("Timeout error occurred when entering password")
        os.rmdir(new_directory_path)
        driver.quit()

# The above two functions lead us to the function below
def login_page(email, password, wait, driver, new_directory_path):
    username_page(email, wait, driver, new_directory_path)
    password_page(password, wait, driver, new_directory_path)


# Function below clicks on profile and then switches to god mode
def godmode_page(wait, driver, new_directory_path):
    try:
        profile_div = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "info")))
        profile_div.click()
    except TimeoutException:
        print("Timeout error occurred when trying to click profile")
        driver.quit()

    try:
        god_mode_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[.//span[contains(text(), 'Switch to God Mode')]]")))
        god_mode_button.click()
    except TimeoutException:
        print("Timeout error occurred when trying to click godmode")
        os.rmdir(new_directory_path)
        driver.quit()


# Clicks on the first card  to display all eco accounts, then selects ecoaccount  environment. i.e. MyBookings, Corporate, Operations
def ecoaccount_page(ecoaccount, wait, driver, new_directory_path):
    try:
        overlay_uvicon = (By.CLASS_NAME, "uv-loader-uvicon")
        wait.until(ec.invisibility_of_element_located(overlay_uvicon))
        eco_accounts_div = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "card-accounts")))
        eco_accounts_div.click()
    except TimeoutException:
        print("Timeout error occurred when trying to displaying all possible ecoaccounts")
        os.rmdir(new_directory_path)
        driver.quit()

    try:
        eco_account_corporate = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, ecoaccount)))
        eco_account_corporate.click()
    except TimeoutException:
        print("Timeout error occurred when trying to select ecoaccount")
        os.rmdir(new_directory_path)
        driver.quit()

# Selects the indicated  venue
def venue_page(venue, wait, driver, new_directory_path):
    try:
        venue = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[text()='" + venue + "']")))
        venue.click()
    except TimeoutException:
        print("Timeout error occurred when trying to enter correct venue")
        os.rmdir(new_directory_path)
        driver.quit()


# Selects the required category and report on the report selection page
def select_report_page(category, report, wait, driver, new_directory_path):
    try:
        report_dropdown = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[.//span[text()='" + category + "']]")))
        report_dropdown.click()
    except TimeoutException:
        print("Timeout error occurred when selecting report category")
        os.rmdir(new_directory_path)
        driver.quit()

    try:
        thereport = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-item' and text()='" + report + "']")))
        thereport.click()
    except TimeoutException:
        print("Timeout error occurred when selecting report from the dropdown")
        os.rmdir(new_directory_path)
        driver.quit()


# Selects the filter, then just clicks save, updates the url so that it can be changed
def filter_trick_page(wait, driver, new_directory_path):
    try:
        datefilter = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "fa-filter")))
        datefilter.click()
    except TimeoutException:
        print("Timeout error occurred when selecting filter in the filter-trick")
        driver.quit()

    try:
        save_button = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "btn-primary")))
        save_button.click()
    except TimeoutException:
        print("Timeout error occurred when selecting save on the datefilter popup")
        os.rmdir(new_directory_path)
        driver.quit()


# Acquires and parses current url, modifies query paramters, creates new URL, then clicks download button
def update_url_date_page(fromdate, todate, driver, new_directory_path):
    try:
        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)
        if 'caldate' in query_params:
            query_params['caldate'] = [fromdate]
        elif 'fromcaldate' in query_params:
            query_params['fromcaldate'] = [fromdate]
        query_params['tocaldate'] = [todate]
        updated_query = urlencode(query_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, updated_query, parsed_url.fragment))
        driver.get(new_url)
        click_download_button(driver)
    except TimeoutException:
        print("Timeout error occurred when altering url")
        print("URL Before this step:" + current_url)
        print("URL After the failed step:" + new_url)
        os.rmdir(new_directory_path)
        driver.quit()

# Saves report into dataframe, removes file from newly made directory, then removes the directory, only if it is empty
def acquire_report(new_directory_path, driver):
    try:
        downloaded_file = wait_for_download_complete(new_directory_path)
        file_path = os.path.join(new_directory_path, downloaded_file)
        df = pd.read_excel(file_path)
        os.remove(file_path)
        os.rmdir(new_directory_path)
        driver.quit()
        return df
    except TimeoutException:
        os.rmdir(new_directory_path)
        print("WebDriverException occurred. The driver may not exist.")
        return None
