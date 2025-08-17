import getpass
from database import create_connection, close_connection

def register_user():
    """
    Register a new user
    """
    print("\n--- Registro de Usuario ---")
    
    # Get user input
    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    email = input("Email: ").strip().lower()
    
    while True:
        password = getpass.getpass("Contraseña: ").strip()
        confirm_password = getpass.getpass("Confirmar contraseña: ").strip()
        
        if password != confirm_password:
            print("Las contraseñas no coinciden. Intente nuevamente.")
        else:
            break
    
    # Insert user into database
    connection = create_connection()
    if not connection:
        print("Error al conectar a la base de datos.")
        return None
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO usuario (nombres, apellidos, email, password) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nombres, apellidos, email, password))
        connection.commit()
        user_id = cursor.lastrowid
        print("\n¡Usuario registrado exitosamente!")
        return user_id
        
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return None
        
    finally:
        cursor.close()
        close_connection(connection)

def login_user():
    """
    Authenticate a user
    """
    print("\n--- Inicio de Sesión ---")
    
    email = input("Email: ").strip().lower()
    password = getpass.getpass("Contraseña: ").strip()
    
    connection = create_connection()
    if not connection:
        print("Error al conectar a la base de datos.")
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT id_usuario, nombres, apellidos, email 
        FROM usuario 
        WHERE email = %s AND password = %s
        """
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        
        if user:
            print(f"\n¡Bienvenido, {user['nombres']} {user['apellidos']}!")
            return user['id_usuario']
        else:
            print("\nCredenciales incorrectas. Intente nuevamente.")
            return None
            
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None
        
    finally:
        cursor.close()
        close_connection(connection)
