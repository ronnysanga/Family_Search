import getpass
from typing import Optional, Dict, Any
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.auth.login_service import authenticate_user
from services.person import get_person_by_user_id

def show_login_form() -> Optional[Dict[str, Any]]:
    """
    Display login form and handle user authentication.
    
    Returns:
        Dictionary with user data if authentication is successful, None otherwise
    """
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        clear_screen()
        show_header("Inicio de Sesión")
        
        # Show remaining attempts
        if attempts > 0:
            show_message(f"Intento {attempts + 1} de {max_attempts}", "info")
        
        # Get user input
        email = get_input("\nCorreo electrónico (o 'salir' para volver al menú principal): ").strip().lower()
        
        # Allow user to exit
        if email.lower() == 'salir':
            return None
            
        if not email:
            show_message("El correo electrónico es requerido.", "error")
            input("Presione Enter para continuar...")
            attempts += 1
            continue
            
        password = getpass.getpass("Contraseña: ").strip()
        
        if not password:
            show_message("La contraseña es requerida.", "error")
            input("Presione Enter para continuar...")
            attempts += 1
            continue
            
        # Authenticate user
        user = authenticate_user(email, password)
        
        if user:
            # Get person data if exists
            person = get_person_by_user_id(user['id_usuario'])
            if person:
                user.update({
                    'id_persona': person['id_persona'],
                    'es_persona': True
                })
            else:
                user['es_persona'] = False
                
            show_message(f"¡Bienvenido, {user['nombres']}!", "success")
            return user
            
        # Authentication failed
        attempts += 1
        if attempts < max_attempts:
            show_message("\nCredenciales inválidas. Por favor intente nuevamente.", "error")
            input("Presione Enter para continuar...")
    
    # Max attempts reached
    show_message("\nNúmero máximo de intentos alcanzado. Por favor intente más tarde.", "error")
    input("Presione Enter para volver al menú principal...")
    return None
