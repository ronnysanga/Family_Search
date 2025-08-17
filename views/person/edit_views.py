from services.person import search_people, edit_person
from utils.console_utils import show_header, show_message, get_input, clear_screen
from .search_views import search_and_select_person

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
        sexo = person.get('sexo', '').lower()
        sexo_display = 'No especificado'
        if sexo == 'masculino' or sexo == 'm':
            sexo_display = 'Masculino'
        elif sexo == 'femenino' or sexo == 'f':
            sexo_display = 'Femenino'
        print(f"5. Sexo: {sexo_display}")
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
                print("\nOpciones de sexo (deje en blanco para no cambiar):")
                print("1. Masculino")
                print("2. Femenino")
                opcion = input("Seleccione una opción (1-2, ENTER para no cambiar): ").strip()
                if opcion == '1':
                    person['sexo'] = 'masculino'
                    break
                elif opcion == '2':
                    person['sexo'] = 'femenino'
                    break
                elif not opcion:
                    break
                show_message("Por favor ingrese una opción válida.", "error")
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
