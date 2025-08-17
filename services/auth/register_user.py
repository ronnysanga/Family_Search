from database import create_connection, close_connection
from utils.console_utils import show_message
from services.person import add_person

def register_user(user_data):
    connection = create_connection()
    if not connection:
        show_message("Error al conectar a la base de datos.", "error")
        return None
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO usuario (nombres, apellidos, email, password) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_data['nombres'],
            user_data['apellidos'],
            user_data['email'],
            user_data['password']
        ))
        connection.commit()
        user_id = cursor.lastrowid
        
        # Crear automáticamente un perfil de persona para el usuario
        person_data = {
            'nombres': user_data['nombres'],
            'apellidos': user_data['apellidos'],
            'sexo': user_data.get('sexo', 'masculino'),  # Usar el sexo proporcionado o 'masculino' por defecto
            'biografia': 'Perfil creado automáticamente al registrarse.'
        }
        
        if not add_person(person_data, user_id):
            show_message("Usuario registrado, pero hubo un error al crear el perfil de persona.", "warning")
        
        show_message("Usuario registrado exitosamente. Se ha creado su perfil de persona.", "success")
        return user_id
        
    except Exception as e:
        if "Duplicate entry" in str(e):
            show_message("El correo electrónico ya está registrado.", "error")
        else:
            show_message(f"Error al registrar usuario: {e}", "error")
        return None
        
    finally:
        cursor.close()
        close_connection(connection)
