from database import create_connection, close_connection
from utils.console_utils import show_message

def search_people(search_term=None, limit=50):
    connection = create_connection()
    if not connection:
        show_message("Error al conectar a la base de datos.", "error")
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if search_term:
            search_pattern = f"%{search_term}%"
            query = """
            SELECT id_persona, nombres, apellidos, fecha_nacimiento, lugar_nacimiento
            FROM persona
            WHERE nombres LIKE %s OR apellidos LIKE %s
            ORDER BY apellidos, nombres
            LIMIT %s
            """
            cursor.execute(query, (search_pattern, search_pattern, limit))
        else:
            query = """
            SELECT id_persona, nombres, apellidos, fecha_nacimiento, lugar_nacimiento
            FROM persona
            ORDER BY apellidos, nombres
            LIMIT %s
            """
            cursor.execute(query, (limit,))
        
        return cursor.fetchall()
    except Exception as e:
        show_message(f"Error al buscar personas: {e}", "error")
        return []
    finally:
        cursor.close()
        close_connection(connection)
