import getpass
from services.auth.login_user import login_user
from utils.console_utils import show_header, show_message, get_input

def show_login_form():
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
