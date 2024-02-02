# As of right now, this file doesn't work as it needs to be refactored to compensate for the added modularity.
# File for report comparison. Uses multi-threading, utilizing dynamic "task" generation, and headless browsing.

from config.web_credentials import webconfig
from data_access.database_operations import get_total_revenues_breakdown_data, get_booking_and_cancelled_data
from functions.dataframe_analysis import generate_and_compare_reports, compare_reports
import threading
import pandas as pd  # This import ends up being used once some lines of code are dynamically made

# Define a dictionary to store results
report_results = {}

#
# The 50 lines below run outside of main in order to work, as they are executing dynamically made lines on the fly.
#

# Defines the start and end dates
start_date = '2023-01-01'
end_date = '2023-01-27'
# Define & create variables start_date_1 to start_date_12 and end_date_1 to end_date_11
for i in range(1, 2):
    exec(f'start_date_{i} = (pd.to_datetime(start_date) + pd.DateOffset(months=i-1)).strftime("%Y-%m-%d")')
    exec(f'end_date_{i} = (pd.to_datetime(end_date) + pd.DateOffset(months=i-1)).strftime("%Y-%m-%d")')
# Define tasks for report generation and comparison
# Range can be modified to be as low as range(1, 2) for just the first month, and up to range(1, 13) for all year
report_tasks = []

# Define common report_args and official_report_args values
corporate = "box-ecosystem-28"
management = "box-ecosystem-23"
common_report_args = ('UAT', webconfig['email'], webconfig['password'])
common_report_data = [
    (f'{corporate}', 'MGM Corporate', 'Total Revenues', 'Total Revenues Breakdown'),
    (f'{management}', 'MGM Bellagio', 'Bookings', 'Bookings & Cancelled')
]
task_id_counter = 1
for i in range(1, 2):
    start_date_var = f'start_date_{i}'
    end_date_var = f'end_date_{i}'
    start_date_val = locals()[start_date_var]  # Get the value of start_date_i variable
    end_date_val = locals()[end_date_var]  # Get the value of end_date_i variable

    for task_id, (report_type, report_name, report_title, report_subtitle) in enumerate(common_report_data, start=1):
        report_args = (start_date_val, end_date_val, get_total_revenues_breakdown_data) if report_type == corporate else (start_date_val, end_date_val, get_booking_and_cancelled_data)
        official_report_args = common_report_args + (report_type, report_name, report_title, report_subtitle, start_date_val, end_date_val)
        report_tasks.append({'task_id': task_id_counter, 'report_args': report_args, 'official_report_args': official_report_args})
        task_id_counter += 1

# Generates the task description so that output is more readable when processing multiple report comparisons.
task_description_list = []
for task in report_tasks:
    task_id = task['task_id']
    report_args = task['report_args']
    official_report_args = task['official_report_args']
    # Extract relevant information for the task description
    venue = official_report_args[4]
    report_type = official_report_args[-3]
    start_date = official_report_args[-2]
    end_date = official_report_args[-1]
    # Create a custom task description
    task_description = f"Comparing {report_type} for {venue} on {start_date} to {end_date}"
    task_description_list.append(task_description)
    print(task_description)
    print(task)


# Main function
def main():
    # Initialize the threads list
    threads = []
    # {'task_id': 3, 'report_args': (start_date_2, end_date_2, get_total_revenues_breakdown_data), 'official_report_args': ( 'UAT', webconfig['email'], webconfig['password'], corporate, 'MGM Corporate', 'Total Revenues', 'Total Revenues Breakdown', start_date_2, end_date_2)},
    # {'task_id': 4, 'report_args': (start_date_2, end_date_2, get_booking_and_cancelled_data), 'official_report_args': ( 'UAT', webconfig['email'], webconfig['password'], management, 'MGM Bellagio', 'Bookings', 'Bookings & Cancelled', start_date_2, end_date_2)}
    # Create and start threads for each task
    for task in report_tasks:
        thread = threading.Thread(target=generate_and_compare_reports,
                                  args=(report_results, task['task_id'], task['report_args'], task['official_report_args']))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Process and print results
    for task_id, reports in report_results.items():
        python_report = reports['python_report']
        official_report = reports['official_report']
        compare_reports(task_id, task_description_list[task_id - 1], python_report, official_report)


if __name__ == "__main__":
    main()
