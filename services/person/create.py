from database import create_connection, close_connection
from utils.console_utils import show_message

def add_person(person_data, user_id):
    connection = create_connection()
    if not connection:
        show_message("Error al conectar a la base de datos.", "error")
        return None
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO persona (
            id_usuario_creador, nombres, apellidos, 
            fecha_nacimiento, sexo, lugar_nacimiento
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            user_id,
            person_data['nombres'],
            person_data['apellidos'],
            person_data.get('fecha_nacimiento'),
            person_data.get('sexo'),
            person_data.get('lugar_nacimiento')
        ))
        
        connection.commit()
        person_id = cursor.lastrowid
        show_message("Persona agregada exitosamente.", "success")
        return person_id
        
    except Exception as e:
        show_message(f"Error al agregar persona: {e}", "error")
        return None
    finally:
        cursor.close()
        close_connection(connection)
