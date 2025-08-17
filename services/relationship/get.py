from typing import List, Dict, Any, Optional
from database import create_connection, close_connection

def _execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """
    Ejecuta una consulta SQL y devuelve los resultados.
    
    Args:
        query: Consulta SQL a ejecutar
        params: Parámetros para la consulta
        
    Returns:
        Lista de diccionarios con los resultados
    """
    connection = None
    cursor = None
    
    try:
        connection = create_connection()
        if not connection:
            return []
            
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, params or ())
        
        # Obtener resultados
        results = cursor.fetchall()
        
        # Consumir cualquier resultado pendiente
        if cursor.with_rows:
            cursor.fetchall()
            
        return results if results else []
        
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return []
        
    finally:
        # Cerrar cursor y conexión de manera segura
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

def get_relationships(person_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene todas las relaciones de una persona.
    
    Args:
        person_id: ID de la persona
        
    Returns:
        Lista de diccionarios con las relaciones
    """
    query = """
    SELECT 
        rf.id_relacion,
        p2.id_persona as id_pariente,
        CONCAT(p2.nombres, ' ', p2.apellidos) as nombre_pariente,
        rf.tipo_relacion
    FROM relacion_familiar rf
    JOIN persona p1 ON rf.id_persona1 = p1.id_persona
    JOIN persona p2 ON rf.id_persona2 = p2.id_persona
    WHERE rf.id_persona1 = %s
    """
    return _execute_query(query, (person_id,))
