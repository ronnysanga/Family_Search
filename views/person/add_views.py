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
    
    sexo = get_input("Sexo (masculino/femenino, opcional): ", required=False).lower()
    if sexo and sexo in ['masculino', 'femenino']:
        person_data['sexo'] = sexo
    elif sexo:
        show_message("El sexo debe ser 'masculino' o 'femenino'. Campo omitido.", "error")
    
    lugar_nacimiento = get_input("Lugar de nacimiento (opcional): ", required=False)
    if lugar_nacimiento:
        person_data['lugar_nacimiento'] = lugar_nacimiento
    
    return add_person(person_data, user_id)
