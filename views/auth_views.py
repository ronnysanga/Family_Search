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
    """Display the login form."""
    show_header("Inicio de Sesión")
    
    credentials = {
        'email': get_input("Email: ").lower(),
        'password': getpass.getpass("Contraseña: ")
    }
    
    return login_user(credentials)
