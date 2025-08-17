import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Cargar variables de entorno desde .env
load_dotenv()

def get_db_connection():
    """
    Establece y devuelve una conexión a la base de datos MySQL.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('HOSTNAME'),
            port=int(os.getenv('DB_PORT', '3306')),  # Puerto por defecto 3306 para MySQL
            user=os.getenv('USERNAME'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE')
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos MySQL")
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise

def test_connection():
    """
    Prueba la conexión a la base de datos y devuelve el estado.
    """
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_info = cursor.fetchone()
            cursor.close()
            connection.close()
            return {
                "status": "success",
                "message": "Conexión exitosa a la base de datos",
                "database": db_info[0]
            }
    except Error as e:
        return {
            "status": "error",
            "message": f"Error al conectar a la base de datos: {str(e)}"
        }
