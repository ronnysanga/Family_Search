from services.person import get_user_profile
from utils.console_utils import show_header, show_message, get_input

def show_profile(user_id):
    """Display user profile information."""
    show_header("Mi Perfil")
    
    user = get_user_profile(user_id)
    if user:
        print(f"Nombre: {user['nombres']} {user['apellidos']}")
        print(f"Email: {user['email']}")
        print(f"Fecha de registro: {user['fecha_creacion_usuario']}")
    
    input("\nPresione Enter para continuar...")
