# selenium_reporting.py
# File is used for implementing automated web reporting
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from web_automation.functions.web_functions import *
from web_automation.functions.web_data import data_type_mapping
import os
import pandas as pd


# Used if your code works,  same as one below but without debugging fluff
def generateofficialreport(environment, email, password, ecoaccount, account, category, report, fromdate, todate):
    """
        Generates an official report by automating web interactions using Selenium.

        Parameters:
        environment (str): The environment to use (e.g., test, production).
        email (str): Email for login.
        password (str): Password for login.
        ecoaccount (str): Type of ecoaccount ('corporate' or 'management').
        account (str): Account to be used.
        category (str): Report category.
        report (str): Report type.
        fromdate (str): Start date for the report.
        todate (str): End date for the report.

        Returns:
        pd.DataFrame: The data extracted from the report.
    """

    # Set account based on input
    if ecoaccount == 'corporate':
        ecoaccount = 'box-ecosystem-28'
    elif ecoaccount == 'management':
        ecoaccount = 'box-ecosystem-23'
    else:
        ecoaccount = 'box-ecosystem-23'

    # Determine the website based on the environment
    website = set_web_environment(environment)

    # Create a unique (temporary) directory for each report download
    new_directory_path = os.path.join(os.getcwd(), report + account + fromdate)
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)

    # Set Chrome options for headless browsing and file download preferences
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    preferences = {
        "download.default_directory": new_directory_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", preferences)

    # Set up the WebDriver, and initialize a timeout of 10 seconds
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1200, 900)
    wait = WebDriverWait(driver, 30)

    # Go to website
    driver.get(website)

    #############################################################
    ##  Initialize, Operation Auto: ACQUIRING THE REPORT!!!!!! ##
    #############################################################

    login_page(email, password, wait, driver, new_directory_path)
    godmode_page(wait, driver, new_directory_path)
    ecoaccount_page(ecoaccount, wait, driver, new_directory_path)
    venue_page(account, wait, driver, new_directory_path)
    select_report_page(category, report, wait, driver, new_directory_path)
    filter_trick_page(wait, driver, new_directory_path)
    update_url_date_page(fromdate, todate, driver, new_directory_path)
    df = acquire_report(new_directory_path, driver)

    # for column in df.columns:
    # if column in data_type_mapping:
    # df[column] = df[column].astype(data_type_mapping[column])

    for column, data_type in data_type_mapping.items():
        if column in df.columns:
            df[column] = df[column].astype(data_type)

    for column in df.columns:
        if not pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna('')

    return df


# Used for debugging, contains many print statements, and prints url as it changes
def generateofficialreport_debug(environment, email, password, ecoaccount, account, category, report, fromdate, todate):
    # Website for driver, and required credentials
    website = set_web_environment(environment)

    # Unique path for each report download, dynamic directory allocation
    new_directory_path = os.path.join(os.getcwd(), report + account)
    # Create the directory if it doesn't exist
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
    chrome_options = Options()

    preferences = {
        "download.default_directory": new_directory_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", preferences)

    # Set up the WebDriver, and initialize a timeout of 10 seconds
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1200, 900)
    wait = WebDriverWait(driver, 10)

    # Go to website
    driver.get(website)

    #############################################################
    ##  Initialize, Operation Auto: ACQUIRING THE REPORT!!!!!! ##
    #############################################################

    print("Step One: Enter username, press enter")
    email_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[formcontrolname='email']")))
    email_input.send_keys(email + Keys.RETURN)

    print("Step Two: Enter password, press enter")
    password_input = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[formcontrolname='password']")))
    password_input.send_keys(password + Keys.RETURN)

    print("Step Three: Click on profile")
    profile_div = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "info")))
    profile_div.click()

    print("Step Four: Click the 'Switch to God Mode' button (to switch to God Mode, allowing all eco accounts to be accessible")
    god_mode_button = \
        wait.until(ec.element_to_be_clickable((By.XPATH, "//a[.//span[contains(text(), 'Switch to God Mode')]]")))
    god_mode_button.click()

    print("Step Five: Click on the first card, to display all eco accounts")
    overlay_uvicon = (By.CLASS_NAME, "uv-loader-uvicon")
    wait.until(ec.invisibility_of_element_located(overlay_uvicon))
    eco_accounts_div = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "card-accounts")))
    eco_accounts_div.click()

    print("Step Six: Click on Corporate/Management Eco Account")
    eco_account_corporate = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, ecoaccount)))
    eco_account_corporate.click()

    print("Step Six: Click on Corporate Eco Account: ")
    mgm_corporate = \
        wait.until(ec.element_to_be_clickable((By.XPATH, "//a[text()='" + account + "']")))
    mgm_corporate.click()

    print("Step Seven: Click on Required Report Dropdown:")
    report_dropdown = \
        wait.until(ec.element_to_be_clickable((By.XPATH, "//button[.//span[text()='" + category + "']]")))
    report_dropdown.click()

    print("Step Eight: Click on Type of Report")
    thereport = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-item' and text()='" + report + "']")))
    thereport.click()

    print("Step Nine: Select filter, then save to change url")
    datefilter = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "fa-filter")))
    datefilter.click()
    save_button = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "btn-primary")))
    save_button.click()

    print("Step Ten: Acquire and parse current url, modify query paramters, then create new URL")
    current_url = driver.current_url
    print(current_url)
    parsed_url = urlparse(current_url)
    query_params = parse_qs(parsed_url.query)
    if 'caldate' in query_params:
        query_params['caldate'] = [fromdate]
    elif 'fromcaldate' in query_params:
        query_params['fromcaldate'] = [fromdate]
    # query_params['caldate'] = fromdate
    query_params['tocaldate'] = todate
    new_query_string = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query_string))
    driver.get(new_url)
    print(new_url)

    print("Step Eleven: Download report")
    click_download_button(driver)

    print("Step Twelve: Save report into dataframe")
    downloaded_file = wait_for_download_complete(new_directory_path)
    file_path = os.path.join(new_directory_path, downloaded_file)
    df = pd.read_excel(file_path)
    print("Removes the file from the newly made temp directory")
    os.remove(file_path)
    print("Function to remove directory, only if it is empty, to prevent possible catastrophes")
    os.rmdir(new_directory_path)
    driver.quit()

    # Iterate through the columns of the acquired dataframe
    # to ensure accurate data types, and accurate analysis
    #for column, data_type in data_type_mapping.items():
    #    if column in df.columns:
    #        df[column] = df[column].astype(data_type)

    for column in df.columns:
        if column in data_type_mapping:
            df[column] = df[column].astype(data_type_mapping[column])

    #for column in df.columns:
    #    if not pd.api.types.is_numeric_dtype(df[column]):
     #       df[column] = df[column].fillna('')

    return df
