"""
Person retrieval operations.

This module handles all person retrieval operations from the database.
"""
from typing import Dict, Optional
from database import create_connection, close_connection

def get_person_by_id(person_id: int) -> Optional[Dict]:
    """
    Retrieve a person by their ID.
    
    Args:
        person_id: The ID of the person to retrieve
        
    Returns:
        A dictionary containing the person's data, or None if not found
    """
    conn = create_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                p.*,
                DATE_FORMAT(p.fecha_nacimiento, '%d/%m/%Y') as fecha_nac_formateada,
                DATE_FORMAT(p.fecha_defuncion, '%d/%m/%Y') as fecha_def_formateada
            FROM persona p
            WHERE p.id_persona = %s
            """,
            (person_id,)
        )
        person = cursor.fetchone()
        return person if person else None
        
    except Exception as e:
        print(f"Error retrieving person: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(conn)

def get_person_by_user_id(user_id: int) -> Optional[Dict]:
    """
    Retrieve a person by their associated user ID.
    
    Args:
        user_id: The ID of the user associated with the person
        
    Returns:
        A dictionary containing the person's data, or None if not found
    """
    conn = create_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                p.*,
                DATE_FORMAT(p.fecha_nacimiento, '%d/%m/%Y') as fecha_nac_formateada,
                DATE_FORMAT(p.fecha_defuncion, '%d/%m/%Y') as fecha_def_formateada
            FROM persona p
            WHERE p.id_usuario_creador = %s
            """,
            (user_id,)
        )
        person = cursor.fetchone()
        return person if person else None
        
    except Exception as e:
        print(f"Error retrieving person by user ID: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(conn)
