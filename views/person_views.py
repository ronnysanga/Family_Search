from services.person_service import get_user_profile, search_people, add_person, edit_person
from utils.console_utils import show_header, show_message, get_input, clear_screen

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

def search_and_select_person(prompt="Buscar persona"):
    """
    Permite buscar y seleccionar una persona de la base de datos.
    
    Returns:
        dict or None: Información de la persona seleccionada o None si se cancela
    """
    while True:
        clear_screen()
        show_header(prompt)
        search_term = input("Ingrese nombre o apellido (o deje en blanco para ver todos, 'salir' para cancelar): ").strip()
        
        if search_term.lower() == 'salir':
            return None
            
        results = search_people(search_term)
        
        if not results:
            show_message("No se encontraron personas que coincidan con la búsqueda.", "warning")
            input("Presione Enter para continuar...")
            continue
            
        # Mostrar resultados
        clear_screen()
        show_header(f"Resultados de búsqueda ({len(results)})")
        for i, person in enumerate(results, 1):
            birth_info = f" | Nacimiento: {person['fecha_nacimiento'].strftime('%d/%m/%Y')}" if person.get('fecha_nacimiento') else ""
            print(f"{i}. {person['apellidos']}, {person['nombres']}{birth_info}")
            
        # Permitir al usuario seleccionar una persona
        while True:
            try:
                selection = input("\nSeleccione un número (o 0 para buscar de nuevo): ").strip()
                if not selection:
                    continue
                    
                choice = int(selection)
                if choice == 0:
                    break
                elif 1 <= choice <= len(results):
                    return results[choice - 1]
                else:
                    show_message("Número fuera de rango. Intente nuevamente.", "error")
            except ValueError:
                show_message("Por favor ingrese un número válido.", "error")

def show_edit_person_form(user_id):
    """Muestra el formulario para editar una persona existente."""
    # Buscar persona a editar
    person = search_and_select_person("Buscar persona a editar")
    if not person:
        return
        
    while True:
        clear_screen()
        show_header(f"Editando: {person['nombres']} {person['apellidos']}")
        
        # Mostrar información actual
        print("\nInformación actual:")
        print(f"1. Nombres: {person.get('nombres', 'No especificado')}")
        print(f"2. Apellidos: {person.get('apellidos', 'No especificado')}")
        print(f"3. Fecha de nacimiento: {person.get('fecha_nacimiento', 'No especificada')}")
        print(f"4. Lugar de nacimiento: {person.get('lugar_nacimiento', 'No especificado')}")
        print(f"5. Sexo: {person.get('sexo', 'No especificado')}")
        print(f"6. Biografía: {person.get('biografia', 'No especificada')[:50]}{'...' if person.get('biografia') and len(person['biografia']) > 50 else ''}")
        
        print("\n¿Qué campo desea editar? (Ingrese el número, 0 para guardar, 'salir' para cancelar)")
        choice = input("Opción: ").strip().lower()
        
        if choice == 'salir':
            if input("¿Desea descartar los cambios? (s/n): ").lower() == 's':
                return
        elif choice == '0':
            show_message("Cambios guardados exitosamente.", "success")
            return
        elif choice == '1':
            new_value = input("Nuevos nombres: ").strip()
            if new_value:
                person['nombres'] = new_value
        elif choice == '2':
            new_value = input("Nuevos apellidos: ").strip()
            if new_value:
                person['apellidos'] = new_value
        elif choice == '3':
            new_value = input("Nueva fecha de nacimiento (YYYY-MM-DD, deje en blanco para eliminar): ").strip()
            person['fecha_nacimiento'] = new_value if new_value else None
        elif choice == '4':
            new_value = input("Nuevo lugar de nacimiento (deje en blanco para eliminar): ").strip()
            person['lugar_nacimiento'] = new_value if new_value else None
        elif choice == '5':
            while True:
                new_value = input("Nuevo sexo (M/F, deje en blanco para eliminar): ").strip().upper()
                if not new_value or new_value in ['M', 'F']:
                    person['sexo'] = new_value if new_value else None
                    break
                show_message("Por favor ingrese 'M' para masculino o 'F' para femenino.", "error")
        elif choice == '6':
            print("\nBiografía actual (presione Enter dos veces para terminar):")
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            person['biografia'] = '\n'.join(lines) if lines else None
        else:
            show_message("Opción no válida. Intente nuevamente.", "error")
            
        # Actualizar la persona en la base de datos
        if edit_person(person['id_persona'], person, user_id):
            # Actualizar los datos locales con los cambios guardados
            updated_person = search_people(f"id:{person['id_persona']}")
            if updated_person:
                person.update(updated_person[0])
