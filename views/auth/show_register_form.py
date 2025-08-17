from typing import Dict
from utils.console_utils import show_header, get_input, clear_screen

def show_register_form() -> Dict[str, str]:
    """
    Display the registration form and collect user information.
    
    Returns:
        Dict[str, str]: Dictionary containing user registration data
    """
    clear_screen()
    show_header("Registro de Nuevo Usuario")
    print("\nComplete el formulario de registro:")
    
    user_data = {
        'username': get_input("Nombre de usuario: ", required=True),
        'email': get_input("Correo electrónico: ", required=True),
        'password': get_input("Contraseña: ", password=True, required=True, min_length=6),
        'confirm_password': get_input("Confirmar contraseña: ", password=True, required=True)
    }
    
    # Verify password match
    if user_data['password'] != user_data['confirm_password']:
        return {'error': 'Las contraseñas no coinciden'}
    
    return user_data
