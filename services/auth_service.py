from database import create_connection, close_connection
from utils.console_utils import show_message
from .person_service import add_person

def register_user(user_data):
    """
    Register a new user in the database.
    
    Args:
        user_data (dict): Dictionary containing user data (nombres, apellidos, email, password)
        
    Returns:
        int: The ID of the created user, or None if registration failed
    """
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

def login_user(credentials):
    """
    Authenticate a user.
    
    Args:
        credentials (dict): Dictionary containing email and password
        
    Returns:
        dict: User data if authentication is successful, None otherwise
    """
    connection = create_connection()
    if not connection:
        show_message("Error al conectar a la base de datos.", "error")
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT id_usuario, nombres, apellidos, email 
        FROM usuario 
        WHERE email = %s AND password = %s
        """
        cursor.execute(query, (credentials['email'], credentials['password']))
        user = cursor.fetchone()
        
        if user:
            show_message(f"¡Bienvenido, {user['nombres']} {user['apellidos']}!", "success")
            return user
        else:
            show_message("Credenciales incorrectas. Intente nuevamente.", "error")
            return None
            
    except Exception as e:
        show_message(f"Error al iniciar sesión: {e}", "error")
        return None
        
    finally:
        cursor.close()
        close_connection(connection)
