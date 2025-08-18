from typing import Dict, Optional, List, Any
from database import create_connection, close_connection

def _execute_single_query(query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
    """
    Ejecuta una consulta SQL que devuelve un solo resultado.
    
    Args:
        query: Consulta SQL a ejecutar
        params: Parámetros para la consulta
        
    Returns:
        Diccionario con el resultado o None si no se encontraron resultados
    """
    connection = None
    cursor = None
    
    try:
        connection = create_connection()
        if not connection:
            return None
            
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, params or ())
        
        result = cursor.fetchone()
        
        if cursor.with_rows:
            cursor.fetchall()
            
        return result if result else None
        
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return None
        
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print(f"Error al cerrar el cursor: {e}")
            
        try:
            if connection and connection.is_connected():
                close_connection(connection)
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

def get_person_by_id(person_id: int) -> Optional[Dict]:
    """
    Obtiene una persona por su ID.
    
    Args:
        person_id: ID de la persona a buscar
        
    Returns:
        Diccionario con los datos de la persona o None si no se encuentra
    """
    query = """
    SELECT 
        p.*,
        DATE_FORMAT(p.fecha_nacimiento, '%d/%m/%Y') as fecha_nac_formateada,
        DATE_FORMAT(p.fecha_defuncion, '%d/%m/%Y') as fecha_def_formateada
    FROM persona p
    WHERE p.id_persona = %s
    """
    return _execute_single_query(query, (person_id,))

def get_person_by_user_id(user_id: int) -> Optional[Dict]:
    """
    Obtiene una persona por el ID del usuario que la creó.
    
    Args:
        user_id: ID del usuario creador
        
    Returns:
        Diccionario con los datos de la persona o None si no se encuentra
    """
    query = """
    SELECT 
        p.*,
        DATE_FORMAT(p.fecha_nacimiento, '%d/%m/%Y') as fecha_nac_formateada,
        DATE_FORMAT(p.fecha_defuncion, '%d/%m/%Y') as fecha_def_formateada
    FROM persona p
    WHERE p.id_usuario_creador = %s
    """
    return _execute_single_query(query, (user_id,))
