from services.person import add_person
from utils.console_utils import show_header, show_message, get_input

def show_add_person_form(user_id):
    show_header("Agregar Persona")
    
    person_data = {
        'nombres': get_input("Nombres: "),
        'apellidos': get_input("Apellidos: "),
    }
    
    # Campos opcionales
    fecha_nacimiento = get_input("Fecha de nacimiento (YYYY-MM-DD, opcional): ", required=False)
    if fecha_nacimiento:
        person_data['fecha_nacimiento'] = fecha_nacimiento
    
    print("\nOpciones de sexo (opcional):")
    print("1. Masculino")
    print("2. Femenino")
    opcion = get_input("Seleccione una opción (1-2, ENTER para omitir): ").strip()
    if opcion == '1':
        person_data['sexo'] = 'masculino'
    elif opcion == '2':
        person_data['sexo'] = 'femenino'
    
    lugar_nacimiento = get_input("Lugar de nacimiento (opcional): ", required=False)
    if lugar_nacimiento:
        person_data['lugar_nacimiento'] = lugar_nacimiento
    
    return add_person(person_data, user_id)
