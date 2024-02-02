# database_operations.py
import pandas as pd
import logging
from data_access.database_queries import *


# Function for reading query with connection, other functions defined in this file
def execute_query(engine, query):
    try:
        data = pd.read_sql_query(query, engine)
        return data
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return None


####################################################################################

# No Filters exist for Personal Reports -> Logins report, only report needed is corp & management id
def get_personal_reports_logins_data(engine, start_date, end_date):
    query = get_personal_reports_logins_data_query(start_date, end_date)
    return execute_query(engine, query)

#####################################################################################

# Bookings -> Bookings report category
# Only exists in management, so no differentiation between management & corporate needed
def get_booking_summary_data(engine, start_date, end_date):
    query = get_booking_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_booking_and_cancelled_data(engine, start_date, end_date, venid):
    query = get_booking_and_cancelled_data_query(start_date, end_date, venid)
    return execute_query(engine, query)
def get_booking_details_data(engine, start_date, end_date, venid):
    query = get_booking_details_data_query(start_date, end_date, venid)
    return execute_query(engine, query)
def get_promo_codes_data(engine, start_date, end_date):
    query = get_promo_codes_data_query(start_date, end_date)
    return execute_query(engine, query)

# Bookings -> Items report category
# Only exists in management, so no differentiation between management & corporate needed
def get_item_type_summary_data(engine, start_date, end_date):
    query = get_item_type_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_bookings_item_summary_data(engine, start_date, end_date):
    query = get_bookings_item_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_item_details_data(engine, start_date, end_date, venid):
    query = get_item_details_data_query(start_date, end_date, venid)
    return execute_query(engine, query)
def get_item_updates_data(engine, start_date, end_date):
    query = get_item_updates_data_query(start_date, end_date)
    return execute_query(engine, query)

# Bookings -> Carriers report category
# Only exists in management, so no differentiation between management & corporate needed
def get_day_carrier_types_data(engine, start_date, end_date):
    query = get_day_carrier_types_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_day_carrier_bookings_data(engine, start_date, end_date):
    query = get_day_carrier_bookings_data_query(start_date, end_date)
    return execute_query(engine, query)

#######################################################################################

# Payment Gateway -> Gateway (ONLY Corporate)
# A module in payment gateway that ONLY exists in corporate, no need for paramter to determine that
def get_daily_transactions_data(engine, start_date, end_date):
    query = get_daily_transactions_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_daily_summary_data(engine, start_date, end_date):
    query = get_daily_summary_data_query(start_date, end_date)
    return execute_query(engine, query)

# Payment Gateway -> Sales
# Exists in BOTH management & corporate, so parameter determining that is going to be needed
def get_payment_sales_summary_data(engine, start_date, end_date):
     query = get_payment_sales_summary_data_query(start_date, end_date)
     return execute_query(engine, query)
def get_daily_sales_summary_data(engine, start_date, end_date):
    query = get_daily_sales_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_recent_sales_data(engine, start_date, end_date):
    query = get_recent_sales_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_sales_details_data(engine, start_date, end_date, ecosystem, venid):
    query = get_sales_details_data_query(start_date, end_date, ecosystem, venid)
    return execute_query(engine, query)
def get_sales_breakdown_data(engine, start_date, end_date, ecosystem, venid):
    query = get_sales_breakdown_data_query(start_date, end_date, ecosystem, venid)
    return execute_query(engine, query)

# Payment Gateway -> Revenue
# Exists in BOTH management & corporate, so paramter determing that is going to be needed
def get_event_summary_data(engine, start_date, end_date):
    query = get_event_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_breakdown_summary_data(engine, start_date, end_date):
    query = get_breakdown_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_pricing_summary_data(engine, start_date, end_date):
    query = get_pricing_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_book_type_summary_data(engine, start_date, end_date):
    query = get_book_type_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_payment_item_summary_data(engine, start_date, end_date):
    query = get_payment_item_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_owner_summary_data(engine, start_date, end_date):
    query = get_owner_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_item_breakdown_data(engine, start_date, end_date):
    query = get_item_breakdown_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_item_price_points_data(engine, start_date, end_date):
    query = get_item_price_points_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_pay_media_summary_data(engine, start_date, end_date):
    query = get_pay_media_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_future_sales_data(engine, start_date, end_date):
    query = get_future_sales_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_revenue_details_data(engine, start_date, end_date, ecosystem, venid):
    query = get_revenue_details_data_query(start_date, end_date, ecosystem, venid)
    return execute_query(engine, query)
def get_revenue_breakdown_data(engine, start_date, end_date, ecosystem, venid):
    query = get_revenue_breakdown_data_query(start_date, end_date, ecosystem, venid)
    return execute_query(engine, query)

# Payment Gateway -> Adjustments
# Exists in BOTH management & corporate, so parameter determining that is going to be needed
def get_adjustment_details_data(engine, start_date, end_date):
    query = get_adjustment_details_data_query(start_date, end_date)
    return execute_query(engine, query)

# Payment Gateway -> Total Revenues
# Exists in BOTH management & corporate, so parameter determining that is going to be needed
def get_total_event_summary_data(engine, start_date, end_date):
    query = get_total_event_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_total_revenues_details_data(engine, start_date, end_date):
    query = get_total_revenues_details_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_total_revenues_breakdown_data(engine, start_date, end_date):
    query = get_total_revenues_breakdown_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_total_itemized_data(engine, start_date, end_date):
    query = get_total_itemized_data_query(start_date, end_date)
    return execute_query(engine, query)

# Payment Gateway -> GCB Sales
# Exists in BOTH management & corporate, so parameter determing that is going to be neeeded
def get_gcb_sales_summary_data(engine, start_date, end_date):
    query = get_gcb_sales_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_gcb_sales_details_data(engine, start_date, end_date):
    query = get_gcb_sales_details_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_sales_adjustments_data(engine, start_date, end_date):
    query = get_sales_adjustments_data_query(start_date, end_date)
    return execute_query(engine, query)

# Payment Gateway -> GCB Revenues
# Exists in BOTH management & corporate, so paramter determing that is going to be needed
def get_revenue_summary_data(engine, start_date, end_date):
    query = get_revenue_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_gcb_revenue_details_data(engine, start_date, end_date):
    query = get_gcb_revenue_details_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_revenue_adjustments_data(engine, start_date, end_date):
    query = get_revenue_adjustments_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_total_revenue_data(engine, start_date, end_date):
    query = get_total_revenue_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_total_revenue_detail_data(engine, start_date, end_date):
    query = get_total_revenue_detail_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_future_revenue_data(engine, start_date, end_date):
    query = get_future_revenue_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_admission_tendered_data(engine, start_date, end_date):
    query = get_admission_tendered_data_query(start_date, end_date)
    return execute_query(engine, query)

######################################################################################

# CRM -> Emails, Top 100, Top 1,000
# Exists in ONLY management, no parameter needed
def get_emails_data(engine, start_date, end_date):
    query = get_emails_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_emails_top_100_data(engine, start_date, end_date):
    query = get_emails_top_100_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_emails_top_1000_data(engine, start_date, end_date):
    query = get_emails_top_1000_data_query(start_date, end_date)
    return execute_query(engine, query)

#######################################################################################

# Disputes -> Disputes
# Exists in BOTH management & corporate, parameter needed for that
def get_disputes_data(engine, start_date, end_date):
    query = get_disputes_data_query(start_date, end_date)
    return execute_query(engine, query)

#######################################################################################

# Refunds -> Requests, By Transaction, By Event Date
# Exists in ONLY management, no parameter needed
def get_requests_data(engine, start_date, end_date):
    query = get_requests_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_requests_by_transaction_data(engine, start_date, end_date):
    query = get_requests_by_transaction_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_requests_by_event_date_data(engine, start_date, end_date):
    query = get_requests_by_event_date_data_query(start_date, end_date)
    return execute_query(engine, query)

######################################################################################

# POS -> Check Matching
# Exists in ONLY management, no parameter needed
def get_all_checks_data(engine, start_date, end_date):
    query = get_all_checks_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_unmatched_checks_data(engine, start_date, end_date):
    query = get_unmatched_checks_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_matched_checks_data(engine, start_date, end_date):
    query = get_matched_checks_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_matched_parties_data(engine, start_date, end_date):
    query = get_matched_parties_data_query(start_date, end_date)
    return execute_query(engine, query)

# POS -> Ranking Reports
# Exists in ONLY management, parameter not needed
def get_direct_owner_ranking_data(engine, start_date, end_date):
    query = get_direct_owner_ranking_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_all_owners_ranking_data(engine, start_date, end_date):
    query = get_all_owners_ranking_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_originators_ranking_data(engine, start_date, end_date):
    query = get_originators_ranking_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_comp_ranking_data(engine, start_date, end_date):
    query = get_comp_ranking_data_query(start_date, end_date)
    return execute_query(engine, query)

# POS -> Venue Revenues
# Exists in ONLY management, parameter not needed
def get_checktype_overview_data(engine, start_date, end_date):
    query = get_checktype_overview_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_check_category_overview_data(engine, start_date, end_date):
    query = get_check_category_overview_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_tender_overview_data(engine, start_date, end_date):
    query = get_tender_overview_data_query(start_date, end_date)
    return execute_query(engine, query)

#######################################################################################

# Finance Reconciliation -> Dail Summary (Typo on front-end)
# Exists in ONLY corporate, parameter not needed
def get_finance_daily_summary_data(engine, start_date, end_date):
    query = get_finance_daily_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_transaction_details_data(engine, start_date, end_date):
    query = get_transaction_details_data_query(start_date, end_date)
    return execute_query(engine, query)

# Finance Reconciliation -> Bookings
# Exists in ONLY corporate, parameter not needed
def get_bookings_transacted_data(engine, start_date, end_date):
    query = get_bookings_transacted_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_bookings_recorded_data(engine, start_date, end_date):
    query = get_bookings_recorded_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_bookings_revenue_data(engine, start_date, end_date):
    query = get_bookings_revenue_data_query(start_date, end_date)
    return execute_query(engine, query)
# Front-end shows "Bookings Adjusmented", past-tense for Adjustment is Adjusted
def get_bookings_adjusted_data(engine, start_date, end_date):
    query = get_bookings_adjusted_data_query(start_date, end_date)
    return execute_query(engine, query)

# Finance Reconciliation -> Tenders, & 1 Reconciliation
# Exists in ONLY corporate, parameter not needed
def get_tender_detail_data(engine, start_date, end_date):
    query = get_tender_detail_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_tender_summary_data(engine, start_date, end_date):
    query = get_tender_summary_data_query(start_date, end_date)
    return execute_query(engine, query)
def get_revenue_data(engine, start_date, end_date):
    query = get_revenue_data_query(start_date, end_date)
    return execute_query(engine, query)

####################################################################################

# not 100% positive which report the one below belongs to. Just keeping here for now
def get_extended_booking_data(engine, start_date, end_date):
    query = get_extended_booking_data_query(start_date, end_date)
    return execute_query(engine, query)

