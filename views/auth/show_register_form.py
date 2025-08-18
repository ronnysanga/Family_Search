from typing import Dict, Optional, Tuple
from datetime import datetime
from utils.console_utils import show_header, get_input, clear_screen, show_message
from services.user import create_user
from services.person import add_person

def validate_password(password: str) -> Optional[str]:
    """Validate password meets requirements."""
    if len(password) < 6:
        return "La contraseña debe tener al menos 6 caracteres"
    return None

def get_date_input(prompt: str, required: bool = True) -> Optional[str]:
    """Get and validate a date input."""
    while True:
        try:
            date_str = get_input(prompt, required=required)
            if not date_str and not required:
                return None
                
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            show_message("Formato de fecha inválido. Use YYYY-MM-DD", "error")

def get_gender_input() -> Optional[str]:
    """Get and validate gender input."""
    while True:
        print("\nSeleccione el sexo (opcional):")
        print("1. Masculino")
        print("2. Femenino")
        print("3. No especificar")
        choice = get_input("Opción (1-3, ENTER para omitir): ", required=False)
        
        if not choice or choice == '3':
            return None
        elif choice == '1':
            return 'masculino'
        elif choice == '2':
            return 'femenino'
        else:
            show_message("Opción inválida. Intente nuevamente.", "error")

def show_register_form() -> Tuple[bool, str]:
    """
    Display the registration form and handle user registration.
    
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        clear_screen()
        show_header("Registro de Nuevo Usuario")
        print("\nComplete sus datos personales:")
        
        person_data = {
            'nombres': get_input("Nombres: ", required=True).strip(),
            'apellidos': get_input("Apellidos: ", required=True).strip()
        }
        
        fecha_nac = get_date_input("Fecha de nacimiento (YYYY-MM-DD, opcional): ", required=False)
        if fecha_nac:
            person_data['fecha_nacimiento'] = fecha_nac
            
        sexo = get_gender_input()
        if sexo:
            person_data['sexo'] = sexo
            
        lugar_nac = get_input("Lugar de nacimiento (ciudad, país, opcional): ", required=False)
        if lugar_nac:
            person_data['lugar_nacimiento'] = lugar_nac
        
        clear_screen()
        show_header("Creación de Cuenta")
        print("\nAhora cree sus credenciales de acceso:")
        
        user_data = {
            'email': get_input("Correo electrónico: ", required=True).lower().strip(),
            'nombres': person_data['nombres'],
            'apellidos': person_data['apellidos']
        }
        
        while True:
            password = get_input("Contraseña (mínimo 6 caracteres): ", password=True, required=True)
            password_error = validate_password(password)
            if password_error:
                show_message(password_error, "error")
                continue
                
            confirm_password = get_input("Confirmar contraseña: ", password=True, required=True)
            
            if password != confirm_password:
                show_message("Las contraseñas no coinciden. Intente nuevamente.", "error")
                continue
                
            user_data['password'] = password
            break
        
        user_result = create_user(
            email=user_data['email'],
            password=user_data['password'],
            nombres=user_data['nombres'],
            apellidos=user_data['apellidos']
        )
        
        if 'error' in user_result:
            return False, f"Error al crear el usuario: {user_result['error']}"
        
        person_id = add_person(person_data, user_result['user_id'])
        
        if not person_id:
            return False, "Error al crear el perfil de la persona. Por favor, contacte al administrador."
        
        clear_screen()
        show_header("¡Registro Exitoso!")
        show_message("Su cuenta ha sido creada exitosamente.", "success")
        print("\nDetalles de su cuenta:")
        print(f"Nombre: {user_data['nombres']} {user_data['apellidos']}")
        print(f"Correo electrónico: {user_data['email']}")
        print("\nAhora puede iniciar sesión con su correo y contraseña.")
        input("\nPresione Enter para continuar...")
        return True, ""
        
    except KeyboardInterrupt:
        return False, "Registro cancelado por el usuario"
    except Exception as e:
        return False, f"Error en el registro: {str(e)}"
