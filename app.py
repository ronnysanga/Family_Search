import os
import sys
from dotenv import load_dotenv
from auth import register_user, login_user

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_main_menu():
    """Display the main menu and handle user input."""
    while True:
        clear_screen()
        print("=== MENÚ PRINCIPAL ===")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == '1':
            user_id = login_user()
            if user_id:
                show_logged_in_menu(user_id)
        elif choice == '2':
            user_id = register_user()
            if user_id:
                input("\nPresione Enter para continuar...")
        elif choice == '3':
            print("\n¡Hasta luego!")
            sys.exit(0)
        else:
            print("\nOpción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")

def show_logged_in_menu(user_id):
    """Display the menu for logged-in users."""
    while True:
        clear_screen()
        print("=== MENÚ PRINCIPAL ===")
        print("1. Ver perfil")
        print("2. Buscar personas")
        print("3. Agregar persona")
        print("4. Cerrar sesión")
        
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == '1':
            view_profile(user_id)
        elif choice == '2':
            search_people()
        elif choice == '3':
            add_person(user_id)
        elif choice == '4':
            print("\nSesión cerrada exitosamente.")
            input("Presione Enter para continuar...")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")

def view_profile(user_id):
    """Display user profile information."""
    from database import create_connection, close_connection
    
    connection = create_connection()
    if not connection:
        print("Error al conectar a la base de datos.")
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT nombres, apellidos, email, fecha_creacion_usuario 
        FROM usuario 
        WHERE id_usuario = %s
        """
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        if user:
            clear_screen()
            print("=== MI PERFIL ===")
            print(f"Nombre: {user['nombres']} {user['apellidos']}")
            print(f"Email: {user['email']}")
            print(f"Fecha de registro: {user['fecha_creacion_usuario']}")
        else:
            print("Usuario no encontrado.")
            
    except Exception as e:
        print(f"Error al obtener el perfil: {e}")
    finally:
        cursor.close()
        close_connection(connection)
    
    input("\nPresione Enter para continuar...")

def search_people():
    """Search for people in the database."""
    clear_screen()
    print("=== BUSCAR PERSONAS ===")
    search_term = input("Ingrese nombre o apellido (deje en blanco para ver todos): ").strip()
    
    from database import create_connection, close_connection
    
    connection = create_connection()
    if not connection:
        print("Error al conectar a la base de datos.")
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if search_term:
            search_pattern = f"%{search_term}%"
            query = """
            SELECT id_persona, nombres, apellidos, fecha_nacimiento, lugar_nacimiento
            FROM persona
            WHERE nombres LIKE %s OR apellidos LIKE %s
            ORDER BY apellidos, nombres
            """
            cursor.execute(query, (search_pattern, search_pattern))
        else:
            query = """
            SELECT id_persona, nombres, apellidos, fecha_nacimiento, lugar_nacimiento
            FROM persona
            ORDER BY apellidos, nombres
            LIMIT 50
            """
            cursor.execute(query)
        
        people = cursor.fetchall()
        
        clear_screen()
        print(f"=== RESULTADOS DE BÚSQUEDA ({len(people)}) ===")
        
        if not people:
            print("No se encontraron personas que coincidan con la búsqueda.")
        else:
            for i, person in enumerate(people, 1):
                birth_info = f"Nacido en {person['lugar_nacimiento']} " if person['lugar_nacimiento'] else ""
                birth_date = f"el {person['fecha_nacimiento'].strftime('%d/%m/%Y')} " if person['fecha_nacimiento'] else ""
                print(f"{i}. {person['apellidos']}, {person['nombres']} - {birth_date}{birth_info}")
    
    except Exception as e:
        print(f"Error al buscar personas: {e}")
    finally:
        cursor.close()
        close_connection(connection)
    
    input("\nPresione Enter para continuar...")

def add_person(user_id):
    """Add a new person to the database."""
    clear_screen()
    print("=== AGREGAR PERSONA ===")
    
    # Get person details
    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD, opcional): ").strip()
    sexo = input("Sexo (masculino/femenino, opcional): ").strip().lower()
    lugar_nacimiento = input("Lugar de nacimiento (opcional): ").strip()
    
    # Validate sexo input
    if sexo and sexo not in ['masculino', 'femenino']:
        print("Error: El sexo debe ser 'masculino' o 'femenino'.")
        input("Presione Enter para continuar...")
        return
    
    from database import create_connection, close_connection
    
    connection = create_connection()
    if not connection:
        print("Error al conectar a la base de datos.")
        return
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO persona (
            id_usuario_creador, nombres, apellidos, 
            fecha_nacimiento, sexo, lugar_nacimiento
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Convert empty strings to None for optional fields
        fecha_nacimiento = fecha_nacimiento if fecha_nacimiento else None
        sexo = sexo if sexo else None
        lugar_nacimiento = lugar_nacimiento if lugar_nacimiento else None
        
        cursor.execute(query, (
            user_id, nombres, apellidos, 
            fecha_nacimiento, sexo, lugar_nacimiento
        ))
        
        connection.commit()
        print("\n¡Persona agregada exitosamente!")
        
    except Exception as e:
        print(f"Error al agregar persona: {e}")
    finally:
        cursor.close()
        close_connection(connection)
    
    input("\nPresione Enter para continuar...")

def main():
    """Main function to start the application."""
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Error: No se encontró el archivo .env")
        print("Por favor, cree un archivo .env basado en .env.example")
        return
    
    # Load environment variables
    load_dotenv()
    
    # Start the application
    show_main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
        sys.exit(0)
