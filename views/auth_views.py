import getpass
from services.auth_service import register_user, login_user
from utils.console_utils import show_header, show_message, get_input

def show_register_form():
    """Display the user registration form."""
    show_header("Registro de Usuario")
    
    user_data = {
        'nombres': get_input("Nombres: "),
        'apellidos': get_input("Apellidos: "),
        'email': get_input("Email: ").lower(),
    }
    
    # Pedir el sexo con validación
    while True:
        sexo = get_input("Sexo (M para masculino, F para femenino): ").strip().upper()
        if sexo == 'M':
            user_data['sexo'] = 'masculino'
            break
        elif sexo == 'F':
            user_data['sexo'] = 'femenino'
            break
        else:
            show_message("Por favor ingrese 'M' para masculino o 'F' para femenino.", "error")
    
    while True:
        password = getpass.getpass("Contraseña: ")
        confirm_password = getpass.getpass("Confirmar contraseña: ")
        
        if password != confirm_password:
            show_message("Las contraseñas no coinciden. Intente nuevamente.", "error")
        else:
            user_data['password'] = password
            break
    
    return register_user(user_data)

def show_login_form():
    """Display the login form and handle user authentication."""
    while True:
        show_header("Inicio de Sesión")
        
        email = get_input("Email (o 'salir' para volver al menú principal): ").lower()
        
        # Permitir al usuario salir del formulario de inicio de sesión
        if email == 'salir':
            return None
            
        if not email:  # Si el usuario presiona Enter sin ingresar nada
            continue
            
        password = getpass.getpass("Contraseña: ")
        
        if not password:
            show_message("La contraseña es requerida.", "error")
            input("Presione Enter para continuar...")
            continue
            
        credentials = {
            'email': email,
            'password': password
        }
        
        user = login_user(credentials)
        if user:
            return user
            
        # Si llegamos aquí, la autenticación falló
        show_message("Credenciales inválidas. Por favor intente nuevamente.", "error")
        input("Presione Enter para continuar...")
