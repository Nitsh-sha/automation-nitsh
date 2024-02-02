from report_generation.generate_report import report
from web_automation.selenium_reporting import generateofficialreport
from config.web_credentials import webconfig
from data_access.database_operations import get_total_revenues_breakdown_data, get_booking_and_cancelled_data
import threading

# Define a dictionary to store results
report_results = {}

def generate_and_compare_reports(task_id_param, report_args, official_report_args):
    """
    Generate reports using provided arguments and store them in the report_results dictionary.
    """
    global report_results
    python_report_temp = report(*report_args)
    official_report_temp = generateofficialreport(*official_report_args)
    # Store the generated reports in the report_results dictionary
    report_results[task_id_param] = {'python_report': python_report_temp, 'official_report': official_report_temp}


# Function to compare reports and print results
def compare_reports(task_id, python_report, official_report):
    """
    Compare two reports and print a detailed comparison along with match percentage.
    This function first checks if the reports have the same shape. If they do,
    it then checks for equality. If reports are not identical, it performs a detailed
    comparison and calculates the match percentage.
    """
    print(f"\nComparing Task {task_id} Reports:")
    
    try:
        # Check if both reports have the same number of rows and columns
        if python_report.shape != official_report.shape:
            print("Reports differ in shape.")
            print(f"Python Report Shape: {python_report.shape}")
            print(f"Official Report Shape: {official_report.shape}")
            return
        
        # Check if reports are exactly the same
        if python_report.equals(official_report):
            print("Reports are identical.")
            return

        # Perform a detailed comparison if reports are not identical
        differences = python_report.compare(official_report)
        num_differences = differences.shape[0]
        total_elements = python_report.size
        match_percentage = ((total_elements - num_differences) / total_elements) * 100
        
        # Print the detailed differences and match percentage
        if not differences.empty:
            print(f"Reports differ in {num_differences} elements. Match Percentage: {match_percentage}%")
            print("First 5 differences:")
            print(differences.head())
        else:
            print("Reports are not identical, but no direct differences found. Possible difference in data types or order.")
    
    except Exception as e:
        print(f"An error occurred while comparing reports: {e}")



# Main function
def main():
    # Initialize the threads list
    threads = []

    # Allow user to choose between corporate or management report
    selection = input("Choose report type (corporate/management): ").strip().lower()
    if selection not in ['corporate', 'management']:
        print("Invalid selection. Please choose 'corporate' or 'management'.")
        return

    # Define start and end dates
    start_date = '2023-10-20'
    end_date = '2023-11-20'
    # Determine the entity and entity name based on user selection
    entity = "box-ecosystem-28" if selection == 'corporate' else "box-ecosystem-23"
    entity_name = "MGM Corporate" if selection == 'corporate' else "MGM Bellagio"
    report_type = "Total Revenues" if selection == 'corporate' else "Bookings"

    # Define tasks for report generation and comparison
    report_tasks = [
        {'task_id': 1, 'report_args': (start_date, end_date, get_total_revenues_breakdown_data if selection == 'corporate' else get_booking_and_cancelled_data), 'official_report_args': ('UAT', webconfig['email'], webconfig['password'], entity, entity_name, report_type, report_type + ' Breakdown', start_date, end_date)}
    ]
    
    # Create and start threads for each task
    for task in report_tasks:
        thread = threading.Thread(target=generate_and_compare_reports, args=(task['task_id'], task['report_args'], task['official_report_args']))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Process and print results
    for task_id, reports in report_results.items():
        python_report = reports['python_report']
        official_report = reports['official_report']
        # Compare and print the results of the reports
        compare_reports(task_id, python_report, official_report)

if __name__ == "__main__":
    main()
