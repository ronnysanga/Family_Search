from services.person_service import get_user_profile, search_people, add_person
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

def show_search_people():
    """Display the people search interface."""
    show_header("Buscar Personas")
    search_term = input("Ingrese nombre o apellido (deje en blanco para ver todos): ").strip()
    
    results = search_people(search_term)
    
    show_header(f"Resultados de Búsqueda ({len(results)})")
    
    if not results:
        show_message("No se encontraron personas que coincidan con la búsqueda.")
    else:
        for i, person in enumerate(results, 1):
            birth_info = f"Nacido en {person['lugar_nacimiento']} " if person['lugar_nacimiento'] else ""
            birth_date = f"el {person['fecha_nacimiento'].strftime('%d/%m/%Y')} " if person['fecha_nacimiento'] else ""
            print(f"{i}. {person['apellidos']}, {person['nombres']} - {birth_date}{birth_info}")
    
    input("\nPresione Enter para continuar...")

def show_add_person_form(user_id):
    """Display the form to add a new person."""
    show_header("Agregar Persona")
    
    person_data = {
        'nombres': get_input("Nombres: "),
        'apellidos': get_input("Apellidos: "),
    }
    
    # Optional fields
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
