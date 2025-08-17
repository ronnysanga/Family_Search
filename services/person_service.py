from database import create_connection, close_connection
from utils.console_utils import show_message

def get_user_profile(user_id):
    """
    Retrieve user profile information.
    
    Args:
        user_id (int): The ID of the user
        
    Returns:
        dict: User profile data if found, None otherwise
    """
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

def search_people(search_term=None, limit=50):
    """
    Search for people in the database.
    
    Args:
        search_term (str, optional): Term to search in names or last names
        limit (int, optional): Maximum number of results to return
        
    Returns:
        list: List of matching people, or empty list if none found
    """
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

def add_person(person_data, user_id):
    """
    Add a new person to the database.
    
    Args:
        person_data (dict): Dictionary containing person data
        user_id (int): ID of the user creating the person
        
    Returns:
        int: ID of the created person if successful, None otherwise
    """
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
