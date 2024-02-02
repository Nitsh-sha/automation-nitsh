# report_generation/generate_report.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from web_automation.functions.web_data import data_type_mapping
from logging import error, info
from report_generation.tunnel import create_ssh_tunnel
import pandas as pd
import numpy as np
import re
import os
import time


# Helper function for report
def generatereport(query_function, db_name, startdate, enddate, ecosystem, venid):
    ssh_tunnel = None
    try:
        # create_ssh_tunnel(db_name) returns (engine, tunnel)
        engine, ssh_tunnel = create_ssh_tunnel(db_name)
        info("SSH tunnel established successfully.")

        # data = query_function(engine, startdate, enddate, ecosystem, venid)
        # Call the query function with appropriate arguments
        # If ecosystem is default, this means you are calling a query that only uses one
        # ecosystem, either management or corporate, in this case, just use the default
        # ecosystem by not passing it as a parameter since it is already hard-coded in
        if ecosystem != 'default':
            data = query_function(engine, startdate, enddate, ecosystem, venid)
        else:
            data = query_function(engine, startdate, enddate, venid)

        if data is not None:
            print(f"Report from {db_name}, internally titled {query_function.__name__}:")
            return data
        else:
            error(f"No data returned from database {db_name}")
            return None

    except Exception as e:
        error(f"An error occurred: {e}", exc_info=True)
        return None
    finally:
        # Close the SSH tunnel after the query
        if ssh_tunnel is not None:
            ssh_tunnel.stop()
            info("SSH tunnel closed.")


# could be more efficient by removing the requirement to check the capitalization of the first occurence,
# and rather store what the column names should be and then map that onto the output. Seems to work in matching.
def parse_and_update_breakdown(dataframe):
    new_columns_data = {}
    column_name_style = {}  # To store the first occurrence capitalization

    for index, row in dataframe.iterrows():
        parts = row['BreakDown'].split('|')

        for part in parts:
            match = re.match(r"^([^:]+):([^:]+):(.+)$", part)
            if match:
                original_name = match.group(1)
                lowercase_name = original_name.lower()
                value = match.group(2)
                formatted_value = f"{float(value):.2f}"

                # Initialize column with default values
                if lowercase_name not in new_columns_data:
                    new_columns_data[lowercase_name] = ["0"] * len(dataframe)
                    column_name_style[lowercase_name] = original_name  # Store the first occurrence capitalization

                new_columns_data[lowercase_name][index] = formatted_value

    # Add the new columns to the dataframe using the stored capitalization
    for lowercase_name, values in new_columns_data.items():
        styled_name = column_name_style[lowercase_name]
        dataframe[styled_name] = values

    return dataframe


# Helper function that retrieves the precision of a number
def get_precision(number):
    if isinstance(number, (int, float)):
        decimal_part = str(number).split(".")[1]
        return len(decimal_part) if len(decimal_part) > 0 else 0
    else:
        return 0  # Return 0 for non-numeric values


# Function used for determining how much to round certain columns that are generally made dynamically.
def apply_custom_rounding(column_name, value):
    rounding_precision = {
        'LET Tax': 2,  # LET Tax is rounded to 2 decimal places always. 0 is always 0.00
        'Processing Fee': 1,  # Processing Fee is always 1 decimal places. 0 is always 0.0
        'Subtotal': 0,  # Subtotal is always 0 decimal places, will investigate further. 0 is always 0
        'Total': 2,  # Total is always 2 decimal places. 0 is always 0.00
        # Add more column names and corresponding precision here as new fields are added to database
        # or when new fields are found
    }
    # Convert the value to a float if it's not already numeric
    if not pd.api.types.is_numeric_dtype(value):
        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0  # Default rounding if an error occurs

    # Check if the original precision is greater than the specified precision
    original_precision = get_precision(value)
    specified_precision = rounding_precision.get(column_name, 0)
    if original_precision > specified_precision:
        return value  # Retain the original precision
    else:
        return round(value, specified_precision)

def format_date_columns(df, columns, date_format='%Y-%m-%d'):
    """
    Format specified date columns in the DataFrame to the specified date_format.

    Parameters:
    df (pd.DataFrame): The DataFrame to format.
    columns (list): A list of column names to format as date columns.
    date_format (str): The desired date format (default is '%Y-%m-%d').

    Returns:
    pd.DataFrame: The DataFrame with formatted date columns.
    """
    formatted_df = df.copy()
    for col in columns:
        if col in formatted_df.columns:
            formatted_df[col] = pd.to_datetime(formatted_df[col]).dt.strftime(date_format)
    return formatted_df


# Creates the report by first calling generate report, which returns an entire sql query,
# then it does exception handling, and adds/subtracts columns based off of several factors
# Main report generation function
def report(start_date, end_date, query, ecosystem, venid):
    # Generate the report by calling the generatereport function
    # It establishes an SSH tunnel, runs the SQL query and returns the data
    data = generatereport(query, "PAY", start_date, end_date, ecosystem, venid)

    # If data is empty (no rows), return it immediately
    if data.empty:
        print("No data returned from generatereport")
        # data = pd.DataFrame()
        return data
    # Handling specific queries with additional formatting requirements
    # Will probably split off into seperate custom functions for each different query
    if query.__name__ == 'get_total_revenues_breakdown_data' or query.__name__ == 'get_revenue_breakdown_data'\
            or query.__name__ == 'get_sales_breakdown_data':
        # Update Auth column, and formats date columns in the query
        data['Auth Code'] = pd.to_numeric(data['Auth Code'], errors='coerce')
        date_columns = ['Trans Date', 'Event Date']
        data = format_date_columns(data, date_columns)

        # Parse breakdown, locate index of breakdown, split data frame, sort second part alphabetically
        data = parse_and_update_breakdown(data)
        breakdown_index = data.columns.get_loc('BreakDown')
        columns_before_breakdown = data.iloc[:, :breakdown_index + 1]
        columns_after_breakdown = data.iloc[:, breakdown_index + 1:]

        # Apply custom rounding to the columns after 'BreakDown'
        columns_after_breakdown = columns_after_breakdown.apply(
            lambda columns: columns.map(
                lambda x: apply_custom_rounding(columns.name.lower(), x) if isinstance(columns.name, str) else x),
            axis=0  # Use axis=0 to apply the function column-wise
        )
        # Sort columns that are to the right of BreakDown, concatenate them back, then return
        columns_after_breakdown = columns_after_breakdown.reindex(sorted(columns_after_breakdown.columns), axis=1)
        sorted_data = pd.concat([columns_before_breakdown, columns_after_breakdown], axis=1)

        # Logic below is for sales breakdown, but my apply to other breakdowns, will have to check.
        # Calculates merchant fee based off of two columns in the breakdown column after they are calculated
        # If one of those columns are not present though, all values in that column is set to 0
        if query.__name__ == 'get_sales_breakdown_data':
            if 'ccfee' in data.columns and 'UV App Fee' in data.columns:
                data['Merchant Fee'] = data['UV App Fee'] - data['ccfee']
        return sorted_data

    elif query.__name__ == 'get_booking_and_cancelled_data' or query.__name__ == 'get_booking_details_data' or query.__name__ == 'get_item_details_data'\
            or query.__name__ == 'get_sales_details_data':
        # Defines the specific values to check for dropping irrelevant columns
        values_to_check = [0, '0h', '0m', np.nan, ':', '', ' ']
        # Iterate over the columns and check the condition
        # 1. If a column contains a value within it that is not in values_to_check, then the column stays
        # 2. If not, drop the column
        # cols_to_drop = []
        # for col in data.columns:
        #    if data[col].apply(lambda x: x in values_to_check or pd.isna(x)).all():
        #        cols_to_drop.append(col)

        # Exclude ecozone from the drop list, because for some reason even if it is all 0, it is still shown on front-end.
        cols_to_drop = [col for col in data.columns if
                        col != "EcoZone" and data[col].apply(lambda x: x in values_to_check or pd.isna(x)).all()]

        data.drop(columns=cols_to_drop, inplace=True)
        data = format_date_columns(data, ['Event Date'])
        for column in data.columns:
            if not pd.api.types.is_numeric_dtype(data[column]):
                data[column] = data[column].fillna('')

        return data
    # data.columns = data.columns.str.replace(' ', '_')
    elif query.__name__ == 'get_revenue_details_data':
        for column in data.columns:
            if column in data_type_mapping:
                data[column] = data[column].astype(data_type_mapping[column])
        data['Auth Code'] = pd.to_numeric(data['Auth Code'], errors='coerce')
        data['Card Token'] = pd.to_numeric(data['Card Token'], errors='coerce')
        date_columns = ['Trans Date', 'Event Date']
        data = format_date_columns(data, date_columns)

    # data = data.astype(data_type_mapping)
    # data.columns = data.columns.str.replace('_', ' ')
    # For all other queries, by default, return the data as is
    return data


# Legacy function - used to be used as a wait-to-download function
def wait_for_download(directory):
    initial_files = set(os.listdir(directory))
    start_time = time.time()
    while True:
        current_files = set(os.listdir(directory))
        new_files = current_files - initial_files
        if new_files:
            return new_files.pop()  # Return the name of the new file
        elif time.time() - start_time > 30:  # 30 seconds timeout
            raise Exception("Timeout: No file downloaded")
        time.sleep(1)


# Updated wait_for_download function, now checks the file extension,
# ensuring it does not attempt to download the file too soon
def wait_for_download_complete(directory, timeout=60):
    end_time = time.time() + timeout
    while True:
        xlsx_files = [f for f in os.listdir(directory) if f.endswith(".xlsx")]
        pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
        if xlsx_files:
            return xlsx_files[0]  # Returns the first found .xlsx file
        if pdf_files:
            return pd.DataFrame()
        time.sleep(1)
        if time.time() > end_time:
            raise Exception("Timeout: File download did not complete in the allotted time.")


# Due to the nature of altering the webpage, sometimes the webpage will not properly load, in that case,
# This function will refresh the page (up to 20 times) to ensure it properly loads.
def click_download_button(driver, max_retries=20):
    wait = WebDriverWait(driver, 10)
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Wait for the download button to be clickable and click it
            download = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "fa-download")))
            download.click()
            return  # If successful, exit the function
        except TimeoutException:
            # If the button is not clickable, refresh the page and increase the retry count
            print(f"Button not clickable, refreshing page. Attempt {retry_count + 1} of {max_retries}")
            driver.refresh()
            retry_count += 1

    print("Failed to click the download button after several retries.")
