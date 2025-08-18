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
    
    print("\nOpciones de sexo:")
    print("1. Masculino")
    print("2. Femenino")
    while True:
        opcion = get_input("Seleccione una opción (1-2): ").strip()
        if opcion == '1':
            user_data['sexo'] = 'masculino'
            break
        elif opcion == '2':
            user_data['sexo'] = 'femenino'
            break
        show_message("Opción no válida. Por favor seleccione 1 o 2.", "error")
    
    while True:
        password = getpass.getpass("Contraseña: ")
        confirm_password = getpass.getpass("Confirmar contraseña: ")
        
        if password != confirm_password:
            show_message("Las contraseñas no coinciden. Intente nuevamente.", "error")
        else:
            user_data['password'] = password
            break
    
    return register_user(user_data)