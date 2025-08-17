from typing import List, Dict, Any
from database import create_connection, close_connection

def get_relationships(person_id: int) -> List[Dict[str, Any]]:
    conn = create_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                rf.id_relacion,
                p2.id_persona as id_pariente,
                CONCAT(p2.nombres, ' ', p2.apellidos) as nombre_pariente,
                rf.tipo_relacion
            FROM relacion_familiar rf
            JOIN persona p1 ON rf.id_persona1 = p1.id_persona
            JOIN persona p2 ON rf.id_persona2 = p2.id_persona
            WHERE rf.id_persona1 = %s
            """,
            (person_id,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting relationships: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(conn)

def add_relationship(person1_id: int, person2_id: int, relationship_type: str, user_id: int) -> bool:
    """Add a family relationship between two people"""
    conn = create_connection()
    if not conn:
        return False
        
    try:
        if person1_id == person2_id:
            print("No se puede establecer una relación consigo mismo.")
            show_message("No se puede establecer una relación consigo mismo.", "error")
            return False
            
        cursor = conn.cursor()
        
        # Verificar si la relación ya existe
        cursor.execute(
            """
            SELECT id_relacion FROM relacion_familiar 
            WHERE id_persona1 = %s AND id_persona2 = %s
            """,
            (person1_id, person2_id)
        )
        if cursor.fetchone():
            print("La relación ya existe.")
            return False
            
        # Insertar la relación
        cursor.execute(
            """
            INSERT INTO relacion_familiar 
            (id_persona1, id_persona2, tipo_relacion, id_usuario_creador)
            VALUES (%s, %s, %s, %s)
            """,
            (person1_id, person2_id, relationship_type, user_id)
        )
        conn.commit()
        print("Relación agregada exitosamente.")
        return True
        
    except Exception as e:
        print(f"Error adding relationship: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(conn)
