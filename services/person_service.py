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

def edit_person(person_id, person_data, user_id):
    """
    Edit an existing person's information.
    
    Args:
        person_id (int): ID of the person to edit
        person_data (dict): Dictionary containing updated person data
        user_id (int): ID of the user making the edit
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    connection = create_connection()
    if not connection:
        show_message("Error al conectar a la base de datos.", "error")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Primero, verificar si la persona existe y el usuario tiene permisos
        cursor.execute(
            "SELECT id_persona FROM persona WHERE id_persona = %s AND id_usuario_creador = %s",
            (person_id, user_id)
        )
        if not cursor.fetchone():
            show_message("Persona no encontrada o no tiene permisos para editarla.", "error")
            return False
        
        # Construir la consulta dinámicamente basada en los campos proporcionados
        update_fields = []
        values = []
        
        if 'nombres' in person_data:
            update_fields.append("nombres = %s")
            values.append(person_data['nombres'])
            
        if 'apellidos' in person_data:
            update_fields.append("apellidos = %s")
            values.append(person_data['apellidos'])
            
        if 'fecha_nacimiento' in person_data:
            update_fields.append("fecha_nacimiento = %s")
            values.append(person_data['fecha_nacimiento'])
            
        if 'fecha_defuncion' in person_data:
            update_fields.append("fecha_defuncion = %s")
            values.append(person_data['fecha_defuncion'])
            
        if 'sexo' in person_data:
            update_fields.append("sexo = %s")
            values.append(person_data['sexo'])
            
        if 'lugar_nacimiento' in person_data:
            update_fields.append("lugar_nacimiento = %s")
            values.append(person_data['lugar_nacimiento'])
            
        if 'lugar_defuncion' in person_data:
            update_fields.append("lugar_defuncion = %s")
            values.append(person_data['lugar_defuncion'])
            
        if 'biografia' in person_data:
            update_fields.append("biografia = %s")
            values.append(person_data['biografia'])
        
        if not update_fields:
            show_message("No se proporcionaron datos para actualizar.", "warning")
            return False
            
        # Agregar el ID de la persona al final de los valores
        values.append(person_id)
        
        # Construir y ejecutar la consulta
        query = f"""
        UPDATE persona 
        SET {', '.join(update_fields)}, fecha_actualizacion = CURRENT_TIMESTAMP
        WHERE id_persona = %s
        """
        
        cursor.execute(query, values)
        connection.commit()
        
        if cursor.rowcount > 0:
            show_message("Información de la persona actualizada exitosamente.", "success")
            return True
        else:
            show_message("No se pudo actualizar la información de la persona.", "error")
            return False
            
    except Exception as e:
        show_message(f"Error al actualizar la persona: {e}", "error")
        return False
        
    finally:
        cursor.close()
        close_connection(connection)
