import oracledb
from dotenv import load_dotenv
import os

load_dotenv()

user = os.environ.get('USER')
pas = os.environ.get('PASSWORD')
dns = 'localhost/XEPDB1'


def get_db():

    connection = None

    try:
        connection = oracledb.connect(user=user, password=pas, dsn=dns)
        print('Database Connected!')
        yield connection

    finally:
        if connection:
            connection.close()
