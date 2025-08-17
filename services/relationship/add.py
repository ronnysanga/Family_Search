
from typing import Optional
from database import create_connection, close_connection
from utils.console_utils import show_message

def add_relationship(person1_id: int, person2_id: int, relationship_type: str, user_id: int) -> bool:
    conn = create_connection()
    if not conn:
        return False
        
    try:
        if person1_id == person2_id:
            show_message("No se puede establecer una relación consigo mismo.", "error")
            return False
            
        cursor = conn.cursor()
        
        # Check if the relationship already exists
        cursor.execute(
            """
            SELECT id_relacion FROM relacion_familiar 
            WHERE id_persona1 = %s AND id_persona2 = %s
            """,
            (person1_id, person2_id)
        )
        if cursor.fetchone():
            show_message("Esta relación ya existe.", "warning")
            return False
            
        # Insert the relationship
        cursor.execute(
            """
            INSERT INTO relacion_familiar 
            (id_persona1, id_persona2, tipo_relacion, id_usuario_creador)
            VALUES (%s, %s, %s, %s)
            """,
            (person1_id, person2_id, relationship_type, user_id)
        )
        conn.commit()
        show_message("Relación agregada exitosamente.", "success")
        return True
        
    except Exception as e:
        show_message(f"Error al agregar la relación: {e}", "error")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(conn)
