import getpass
from services.auth.register_user import register_user
from utils.console_utils import show_header, show_message, get_input

def show_register_form():
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