from database import create_connection, close_connection
from utils.console_utils import show_message

def edit_person(person_id, person_data, user_id):
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
            show_message("No tiene permisos para editar esta persona o la persona no existe.", "error")
            return False
        
        # Construir la consulta de actualización dinámicamente
        update_fields = []
        params = []
        
        if 'nombres' in person_data:
            update_fields.append("nombres = %s")
            params.append(person_data['nombres'])
            
        if 'apellidos' in person_data:
            update_fields.append("apellidos = %s")
            params.append(person_data['apellidos'])
            
        if 'fecha_nacimiento' in person_data:
            update_fields.append("fecha_nacimiento = %s")
            params.append(person_data['fecha_nacimiento'])
            
        if 'sexo' in person_data:
            update_fields.append("sexo = %s")
            params.append(person_data['sexo'])
            
        if 'lugar_nacimiento' in person_data:
            update_fields.append("lugar_nacimiento = %s")
            params.append(person_data['lugar_nacimiento'])
        
        # Si no hay campos para actualizar, retornar True
        if not update_fields:
            return True
            
        # Agregar el ID al final de los parámetros para la cláusula WHERE
        params.append(person_id)
        
        # Construir y ejecutar la consulta
        update_query = f"""
        UPDATE persona 
        SET {', '.join(update_fields)}
        WHERE id_persona = %s
        """
        
        cursor.execute(update_query, params)
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
