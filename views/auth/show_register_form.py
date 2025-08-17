from typing import Dict, Optional
from utils.console_utils import show_header, get_input, clear_screen

def show_register_form() -> Dict[str, str]:
    """
    Display the registration form and collect user information.
    
    Returns:
        Dict[str, str]: Dictionary containing user registration data or error message
    """
    clear_screen()
    show_header("Registro de Nuevo Usuario")
    print("\nComplete el formulario de registro:")
    
    # Get user data with validation
    user_data = {
        'nombres': get_input("Nombres: ", required=True),
        'apellidos': get_input("Apellidos: ", required=True),
        'email': get_input("Correo electrónico: ", required=True),
        'password': get_password_input()
    }
    
    return user_data

def get_password_input() -> str:
    """Get and validate password input with confirmation."""
    while True:
        password = get_input("Contraseña (mínimo 6 caracteres): ", password=True, required=True)
        if len(password) < 6:
            print("La contraseña debe tener al menos 6 caracteres.")
            continue
            
        confirm = get_input("Confirmar contraseña: ", password=True, required=True)
        
        if password == confirm:
            return password
        print("\nLas contraseñas no coinciden. Intente nuevamente.\n")
