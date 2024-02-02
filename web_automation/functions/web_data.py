# web_data.py
# The purpose of this file is to contain necessary data about
# 1. Column Data Types
# 2. Venue ID's
# 4. Report sections and types, by name, to be used in automation
# 3. Other data necessary when doing web reporting or other functions

# This ia dictionary, that stores map columns to their desired data types for the purpose of reporting
data_type_mapping = {
    'EcoZone': object,
    'Event': object,
    'Prepaid': float,
    'Agreed': float,
    'Charged': float,
    'qty': float,
    'guests': float,
    'Auth Code': int,
    'Trans ID': int,
    'LET Tax': float,
    'Processing Fee': float,
    'Subtotal': float,
    'Total': float,
}
