# Must create & configure a file with your sql_username, sql_password, & ssh_user
# Name it database_config.py, place it in this folder
db_config = {
    'ssh_host': '34.70.93.65',
    'sql_username': 'username',
    'sql_password': 'password',
    'db_host': '35.188.217.35',
    'ssh_user': 'username',
    'ssh_port': 22022,
    'sql_port': 3306
}

# Must create & configure a file in order to do automated selenium testing, with your urvenue email & password.
# Name it web_credentials.py, place it in this folder
webconfig = {
    'email': 'youremail@urvenue.com',
    'password': 'password',
}

