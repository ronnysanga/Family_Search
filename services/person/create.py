from typing import Dict, Optional
from database import create_connection, close_connection
from utils.console_utils import show_message

def add_person(person_data: Dict, user_id: int) -> Optional[int]:
    conn = create_connection()
    if not conn:
        show_message("Error al conectar a la base de datos.", "error")
        return None
        
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO persona (
            id_usuario_creador, nombres, apellidos, fecha_nacimiento,
            fecha_defuncion, sexo, lugar_nacimiento, lugar_defuncion, biografia
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_id,
            person_data['nombres'],
            person_data['apellidos'],
            person_data.get('fecha_nacimiento'),
            person_data.get('fecha_defuncion'),
            person_data.get('sexo', 'masculino'),
            person_data.get('lugar_nacimiento'),
            person_data.get('lugar_defuncion'),
            person_data.get('biografia')
        ))
        conn.commit()
        person_id = cursor.lastrowid
        show_message("Persona agregada exitosamente.", "success")
        return person_id
        
    except Exception as e:
        show_message(f"Error al agregar persona: {e}", "error")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(conn)
