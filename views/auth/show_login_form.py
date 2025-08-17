from typing import Dict
from utils.console_utils import show_header, get_input, clear_screen

def show_login_form() -> Dict[str, str]:
    """
    Display the login form and collect user credentials.
    
    Returns:
        Dict[str, str]: Dictionary containing username and password
    """
    clear_screen()
    show_header("Iniciar Sesión")
    print("\nIngrese sus credenciales:")
    
    username = get_input("Usuario: ", required=True)
    password = get_input("Contraseña: ", password=True, required=True)
    
    return {
        'username': username,
        'password': password
    }
