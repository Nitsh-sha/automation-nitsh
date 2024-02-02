# report-automations

### To run QA Report Automation
1. Install the required packages by running the following command in your terminal:

`pip install -r requirements.txt`

2. Create & Update the following files with your own credentials in config folder:
   * **database_config.py**
   * **web_credentials.py**


3. Execute one of the following scripts inside of analysis folder:
   * **report_comparator.py**
   * **report_comparatorv1.py**
   * **compare_reports.ipynb**


   File below is used to debug a report when re-creating new ones
   (essentially one on one testing)
   * **report_testing.ipynb**

Notice: As of 1 February 2024 compare_reports jupyter notebook works as well as report_compare.py
