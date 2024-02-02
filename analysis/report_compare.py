# report_compare.py
# The list of all the reports that have been fully completed.

from report_generation.generate_report import report
from web_automation.selenium_reporting import generateofficialreport
from config.web_credentials import webconfig
from data_access.database_operations import get_revenue_breakdown_data, get_revenue_details_data, get_booking_details_data, \
    get_booking_and_cancelled_data, get_item_details_data, get_sales_details_data, get_sales_breakdown_data

from IPython.display import display

start_date, end_date = '2023-10-20', '2023-11-20'

# Use the 2 lines below if debugging a certain report in a jupyter notebook as it adds better visuals.
# import pandas as pd
# pd.set_option('display.max_columns', None), pd.set_option('display.max_rows', None), pd.set_option('display.expand_frame_repr', False)

# PERFECTED = identical across the whole board, perfection is reached.
# WELL DONE = nearly identical on all venues & date ranges, may have an anomaly here or there, data matches 98%+
# DONE = same column names, same # of rows & columns, and most data is present, not necessarily in the exact right order, therefore comparable. Usually 95%+ matching
# IN-PROGRESS = not comparable, not working yet, in the process of being implemented.

# Report list to implement:
# 1. Booking details (DONE)
# 2. Booking and Cancelled (DONE)
# 3. Item details (DONE)
# 4. Sales details (DONE)
# 5. Sales breakdrown (DONE)
# 6. Revenue details (DONE)
# 7. Revenue breakdown (WELL DONE)

# Note: When the fourth argument of the report() function determines the eco-account,
# when 'default' is entered, it just means the report only exists in 1 ecoaccount, so the ecoaccount
# is hardcoded into the query. Do not use 'default' with reports that exist in more than 1 ecoaccount.
# In the web report; however, ecoaccount must always be specified, otherwise it will default to management

# Revenue Details Report DONE (except can't get trans time perfectly yet)
revenues_details_report_mgm_corporate = report(start_date, end_date, get_revenue_details_data, 'corporate', 'MGM Corporate')
display(revenues_details_report_mgm_corporate)
official_revenues_details_report_mgm_corporate = generateofficialreport('UAT', webconfig['email'], webconfig['password'], 'corporate', 'MGM Corporate', 'Revenue', 'Revenue Details', start_date, end_date)
display(official_revenues_details_report_mgm_corporate)

# Revenues Breakdown Report DONE (Event has to be fixed on the web side, created jira ticket AR-1647 in Architecture for it)
revenues_breakdown_report_mgm_corporate = report(start_date, end_date, get_revenue_breakdown_data, 'corporate', 'MGM Corporate')
display(revenues_breakdown_report_mgm_corporate)
official_revenues_breakdown_report_mgm_corporate = generateofficialreport('UAT', webconfig['email'], webconfig['password'], 'corporate', 'MGM Corporate', 'Revenue', 'Revenue Breakdown', start_date, end_date)
display(official_revenues_breakdown_report_mgm_corporate)

# Booking Details Report DONE (Locations column and prepaid status must be fixed)
booking_details_report_mgm_corporate = report(start_date, end_date, get_booking_details_data, 'default', 'MGM Bellagio')
display(booking_details_report_mgm_corporate)
official_booking_details_report_mgm_corporate = generateofficialreport('UAT', webconfig['email'], webconfig['password'], 'management', 'MGM Bellagio', 'Bookings', 'Booking Details', start_date, end_date)
display(official_booking_details_report_mgm_corporate)

# Booking & Cancelled Report DONE (Locations column and prepaid status must be fixed)
booking_and_cancelled_report_mgm_bellagio = report(start_date, end_date, get_booking_and_cancelled_data, 'default', 'MGM Bellagio')
display(booking_and_cancelled_report_mgm_bellagio)
official_booking_and_cancelled_report_mgm_bellagio = generateofficialreport('UAT', webconfig['email'], webconfig['password'], 'management', 'MGM Bellagio', 'Bookings', 'Bookings & Cancelled', start_date, end_date)
display(official_booking_and_cancelled_report_mgm_bellagio)

# Item Details DONE (Most of the contents seem to be there, but the order is definitely very wrong, Locations column also must be fixed)
item_details_report_mgm_bellagio = report(start_date, end_date, get_item_details_data, 'default', 'MGM Bellagio')
display(item_details_report_mgm_bellagio)
official_item_details_report_mgm_bellagio = generateofficialreport('UAT', webconfig['email'], webconfig['password'], 'management', 'MGM Bellagio', 'Items', 'Item Details', start_date, end_date)
display(official_item_details_report_mgm_bellagio)

# Sales details DONE (Trans date and time not in order, and auth code & card token off)
sales_details_report_mgm_bellagio = report(start_date, end_date, get_sales_details_data, 'management', 'MGM Bellagio')
display(sales_details_report_mgm_bellagio)
official_sales_details_report_mgm_bellagio = generateofficialreport('UAT', webconfig['email'], webconfig['password'], 'management', 'MGM Bellagio', 'Sales', 'Sales Details', start_date, end_date)
display(official_sales_details_report_mgm_bellagio)

# Sales breakdown WELL DONE (Almost entirely accurate report by far, very little amount of missing/mismatched fields)
sales_breakdown_report_mgm_bellagio = report(start_date, end_date, get_sales_breakdown_data, 'management', 'MGM Bellagio')
display(sales_breakdown_report_mgm_bellagio)
official_sales_breakdown_report_mgm_bellagio = generateofficialreport('UAT', webconfig['email'], webconfig['password'], 'management', 'MGM Bellagio', 'Sales', 'Sales Breakdown', start_date, end_date)
display(official_sales_breakdown_report_mgm_bellagio)
