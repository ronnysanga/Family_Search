import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def create_connection():
    load_dotenv()
    
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl_ca=os.getenv("SSL_CA_PATH"),
            ssl_disabled=False 
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection, cursor=None):
    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    except:
        pass