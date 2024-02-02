# tunnel.py
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from config.database_config import db_config
import paramiko
from os.path import expanduser
from data_access.database_operations import *
from urllib.parse import quote_plus

logging.basicConfig(level=logging.INFO)

home = expanduser("~")
pkeyfilepath = "/.ssh/roconnections_key"  # Path to your private key
mypkey = paramiko.RSAKey.from_private_key_file(home + pkeyfilepath)

sql_username = db_config['sql_username']
sql_password = db_config['sql_password']
sql_port = db_config['sql_port']  # integer value
ssh_host = db_config['ssh_host']
ssh_user = db_config['ssh_user']
ssh_port = db_config['ssh_port']


# Function is used to establish a tunnel using paramiko and sqlalchemy
# Function is called in the generatereport file & function
def create_ssh_tunnel(db):
    tunnel = SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        remote_bind_address=(db_config['db_host'], sql_port),
    )
    tunnel.start()

    safe_sql_password = quote_plus(sql_password)
    local_port = str(tunnel.local_bind_port)
    connection_string = f"mysql+pymysql://{sql_username}:{safe_sql_password}@localhost:{local_port}/{db}"
    engine = create_engine(connection_string)

    return engine, tunnel
