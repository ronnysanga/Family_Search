from database import create_connection, close_connection
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

print("Usuario que se está usando:", os.getenv("DB_USER"))

conn = create_connection()
if conn and conn.is_connected():
    print("Conectado correctamente a Azure MySQL")
    cur = conn.cursor()
    cur.execute("SELECT NOW(), DATABASE();")
    print("Resultado:", cur.fetchone())
    close_connection(conn, cur)
else:
    print("Conexión fallida")