from services.person import add_person
from utils.console_utils import show_header, show_message, get_input, clear_screen

def show_add_person_form(user_id):
    clear_screen()
    show_header("Agregar Persona")
    
    print("\nComplete los datos de la persona. Los campos marcados con * son obligatorios.")
    
    person_data = {}
    
    person_data['nombres'] = get_input("* Nombres: ", required=True).strip()
    person_data['apellidos'] = get_input("* Apellidos: ", required=True).strip()
    
    print("\n  Fecha de nacimiento (opcional - presione ENTER para omitir): ", end='')
    fecha_nac = input().strip()
    if fecha_nac:
        person_data['fecha_nacimiento'] = fecha_nac
    
    print("\n  Sexo (opcional):")
    print("  1. Masculino")
    print("  2. Femenino")
    print("  3. No especificar")
    print("  Opción (1-3, ENTER para omitir): ", end='')
    opcion = input().strip()
    
    if opcion == '1':
        person_data['sexo'] = 'masculino'
    elif opcion == '2':
        person_data['sexo'] = 'femenino'
    
    print("\n  Lugar de nacimiento (opcional - presione ENTER para omitir): ", end='')
    lugar_nac = input().strip()
    if lugar_nac:
        person_data['lugar_nacimiento'] = lugar_nac
        
    print("\n  Lugar de fallecimiento (opcional - presione ENTER para omitir): ", end='')
    lugar_def = input().strip()
    if lugar_def:
        person_data['lugar_defuncion'] = lugar_def
        
    print("\n  Biografía (opcional - presione ENTER para omitir):")
    print("  ", end='')
    biografia = input().strip()
    if biografia:
        person_data['biografia'] = biografia
    
    clear_screen()
    show_header("Confirmar Datos")
    
    print("\nRevise los datos ingresados:")
    print("-" * 50)
    for key, value in person_data.items():
        if value:
            print(f"{key.capitalize().replace('_', ' ')}: {value}")
    
    confirm = input("\n¿Desea guardar esta persona? (s/n): ").strip().lower()
    if confirm != 's':
        show_message("Operación cancelada.", "info")
        return None
    
    return add_person(person_data, user_id)
