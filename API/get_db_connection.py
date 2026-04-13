import pymssql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return pymssql.connect(
        server=os.getenv('DB_SERVER').replace('tcp:', '').split(',')[0],
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )