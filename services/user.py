from typing import Dict, Any, Optional
from database import create_connection, close_connection
from utils.password_utils import hash_password

def create_user(email: str, password: str, nombres: str, apellidos: str) -> Dict[str, Any]:
    connection = create_connection()
    if not connection:
        return {'error': 'No se pudo conectar a la base de datos'}
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
        if cursor.fetchone():
            return {'error': 'El correo electrónico ya está registrado'}

        hashed_password = hash_password(password)
        
        query = """
        INSERT INTO usuario (email, password, nombres, apellidos, fecha_creacion_usuario)
        VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (email, hashed_password, nombres, apellidos))
        user_id = cursor.lastrowid
        
        connection.commit()
        return {'user_id': user_id}
        
    except Exception as e:
        connection.rollback()
        return {'error': f'Error al crear el usuario: {str(e)}'}
        
    finally:
        cursor.close()
        close_connection(connection)

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user by email.
    
    Args:
        email: User's email
        
    Returns:
        User data as a dictionary or None if not found
    """
    connection = create_connection()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT id_usuario, email, password, nombres, apellidos, 
               DATE_FORMAT(fecha_creacion_usuario, '%%Y-%%m-%%d %%H:%%i:%%s') as fecha_creacion
        FROM usuario 
        WHERE email = %s
        """
        cursor.execute(query, (email,))
        return cursor.fetchone()
        
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)
