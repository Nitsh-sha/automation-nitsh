# analysis/functions dataframe_analysis.py
from report_generation.generate_report import report
from web_automation.selenium_reporting import generateofficialreport
import pandas as pd
import os


# Task function to generate and compare reports.
def generate_and_compare_reports(report_results, task_id_param, report_args, official_report_args):
    """
    Generate reports using provided arguments and store them in the report_results dictionary.
    """
    # global report_results
    python_report_temp = report(*report_args)
    official_report_temp = generateofficialreport(*official_report_args)
    report_results[task_id_param] = {'python_report': python_report_temp, 'official_report': official_report_temp}


# Function to compare reports and print results
def compare_reports(task_id, task_description, python_report, official_report):
    """
    Compare two reports and print a detailed comparison along with match percentage.
    This function first checks if the reports have the same shape. If they do,
    it then checks for equality. If reports are not identical, it performs a detailed
    comparison and calculates the match percentage.
    """
    print(f"\nComparing Task {task_id}, {task_description} Reports:")

    try:
        # Check if both reports have the same number of rows and columns
        if python_report.shape != official_report.shape:
            pd.set_option('display.max_columns', None)
            print("Reports differ in shape.")
            print(f"Python Report Shape: {python_report.shape}")
            print(f"Official Report Shape: {official_report.shape}")

            column_comparison = [python_report.columns[i] == official_report.columns[i] for i in
                                 range(min(len(python_report.columns), len(official_report.columns)))]
            row_count_df1 = len(python_report)
            row_count_df2 = len(official_report)
            # Print the results
            print("Column Name Comparison:", column_comparison)
            print("Number of Rows in DataFrame 1:", row_count_df1)
            print("Number of Rows in DataFrame 2:", row_count_df2)
            return

        # Check if reports are exactly the same
        if python_report.equals(official_report):
            print("Reports are identical. Perfect!")
            return

        # Perform a detailed comparison if reports are not identical
        differences = python_report.compare(official_report)
        num_differences = differences.shape[0]
        total_elements = python_report.size
        match_percentage = ((total_elements - num_differences) / total_elements) * 100

        # Print the detailed differences and match percentage
        if not differences.empty:
            print(f"Reports differ in {num_differences} elements. Match Percentage: {match_percentage}%")
            # print("First 5 differences:")
            # print(differences.head())

        else:
            print(
                "Reports are not identical, but no direct differences found. Possible difference in data types or order.")

    except Exception as e:
        print(f"An error occurred while comparing reports: {e}")

# Function below should be used most frequently in Jupyter Notebooks for QA'ing when investigating individual reports, or creating new ones
def compare_dataframes(df1, df1_name, df2, df2_name):
    """
        Revised dataframe comparator to the one above.
        This function first checks if the reports have the same shape.
        If there are non-matching rows, the 2 dataframes are saved into a xlsx file named after
        the dataframe in the directory test_files.
        It usually returns a string of the result of the analysis.
    """
    # Check if dimensions match
    if df1.shape != df2.shape:
        return f"Dimensions are not equal in atleast shape: {df1.shape} vs {df2.shape}"

    # Check if DataFrames are equal
    if df1.equals(df2):
        return f"DataFrames are perfectly equal!, both have the dimensions {df1.shape}"

    # Find rows where DataFrames differ
    try:
        # Try to compare the two DataFrames
        diff_rows = df1.compare(df2)
        # Check if the comparison result has any differences
        if diff_rows.empty:
            return "No differences found between df1 and df2."
    except ValueError as e:
        # Handle the error when columns do not match
        return "Error: Columns in df1 and df2 do not match.\n" + \
               f"Columns of df1: {', '.join(df1.columns)}\n" + \
               f"Columns of df2: {', '.join(df2.columns)}"

    if not diff_rows.empty:
        folder_name = "test_files"
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        folder_path = os.path.join(parent_dir, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        python_report_path = os.path.join(folder_path, f"{df1_name}.xlsx")
        print(python_report_path)
        official_report_path = os.path.join(folder_path, f"{df2_name}.xlsx")
        df1.to_excel(python_report_path, index=False, engine='openpyxl')
        df2.to_excel(official_report_path, index=False, engine='openpyxl')
        from IPython.display import display
        return f"DataFrames are not equal in contents. Saved both to excel to investigate further if needed. Both have the shape: {df1.shape}. Different rows:\n{display(diff_rows)}"

    if (df1.compare(df2)).empty:
        return f"DataFrames are equal in contents, atleast similar in DTypes, column names, number of columns and number of rows. Match Percentage: 100%"

    # If the dimensions match but there are no differences found, something is unexpected
    return "Unexpected: Dimensions match but DataFrames are not equal, most likely, Dataframes almost perfectly match, but some values are off"
