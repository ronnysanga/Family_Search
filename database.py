import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def create_connection():
    load_dotenv()
    
    try:
        connection = mysql.connector.connect(
            host=os.getenv('HOSTNAME'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('USERNAME'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
