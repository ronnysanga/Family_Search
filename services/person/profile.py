from database import create_connection, close_connection
from utils.console_utils import show_message

def get_user_profile(user_id):
    connection = create_connection()
    if not connection:
        show_message("Error al conectar a la base de datos.", "error")
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT nombres, apellidos, email, fecha_creacion_usuario 
        FROM usuario 
        WHERE id_usuario = %s
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    except Exception as e:
        show_message(f"Error al obtener el perfil: {e}", "error")
        return None
    finally:
        cursor.close()
        close_connection(connection)
