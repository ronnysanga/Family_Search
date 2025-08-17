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
