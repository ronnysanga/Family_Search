from typing import Dict, Any, Optional
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.person.update import edit_person

def show_edit_form(person: Dict[str, Any], user_id: int) -> bool:
    updated_data = person.copy()
    
    while True:
        clear_screen()
        show_header(f"Editar Perfil de {person['nombres']}")
        
        print("\nSeleccione el campo a editar (deje en blanco para terminar):")
        print("1. Nombres")
        print("2. Apellidos")
        print("3. Fecha de Nacimiento")
        print("4. Fecha de Fallecimiento")
        print("5. Lugar de Nacimiento")
        print("6. Lugar de Fallecimiento")
        print("7. Sexo")
        print("8. Biografía")
        
        # Show current values
        print("\nValores actuales:")
        print(f"1. Nombres: {updated_data.get('nombres', '')}")
        print(f"2. Apellidos: {updated_data.get('apellidos', '')}")
        print(f"3. Fecha de Nacimiento: {updated_data.get('fecha_nacimiento', 'No especificada')}")
        print(f"4. Fecha de Fallecimiento: {updated_data.get('fecha_defuncion', 'No especificada')}")
        print(f"5. Lugar de Nacimiento: {updated_data.get('lugar_nacimiento', 'No especificado')}")
        print(f"6. Lugar de Fallecimiento: {updated_data.get('lugar_defuncion', 'No especificado')}")
        # Mostrar el sexo de forma legible
        sexo = updated_data.get('sexo', '').lower()
        sexo_display = 'No especificado'
        if sexo == 'masculino' or sexo == 'm':
            sexo_display = 'Masculino'
        elif sexo == 'femenino' or sexo == 'f':
            sexo_display = 'Femenino'
        print(f"7. Sexo: {sexo_display}")
        print(f"8. Biografía: {updated_data.get('biografia', 'No especificada')[:50]}..." if updated_data.get('biografia') else "8. Biografía: No especificada")
        
        field_choice = get_input("\nOpción: ").strip()
        
        if not field_choice:  # User pressed Enter to finish
            break
            
        # Map choice to field name
        field_map = {
            '1': 'nombres',
            '2': 'apellidos',
            '3': 'fecha_nacimiento',
            '4': 'fecha_defuncion',
            '5': 'lugar_nacimiento',
            '6': 'lugar_defuncion',
            '7': 'sexo',
            '8': 'biografia'
        }
        
        if field_choice not in field_map:
            show_message("Opción no válida. Intente nuevamente.", "error")
            input("Presione ENTER para continuar...")
            continue
            
        field_name = field_map[field_choice]
        
        # Special handling for certain fields
        if field_name == 'sexo':
            while True:
                print("\nOpciones de sexo:")
                print("1. Masculino")
                print("2. Femenino")
                opcion = get_input("Seleccione una opción (1-2): ").strip()
                if opcion == '1':
                    updated_data[field_name] = 'masculino'
                    break
                elif opcion == '2':
                    updated_data[field_name] = 'femenino'
                    break
                show_message("Opción no válida. Por favor seleccione 1 o 2.", "error")
        elif field_name == 'biografia':
            print("\nIngrese la nueva biografía (presione Ctrl+D o Ctrl+Z + ENTER cuando termine):")
            try:
                lines = []
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            updated_data[field_name] = '\n'.join(lines)
        else:
            # For all other fields
            current_value = updated_data.get(field_name, '')
            prompt = f"Nuevo valor (actual: {current_value}): "
            new_value = get_input(prompt)
            if new_value:
                updated_data[field_name] = new_value
    
    # Show changes and confirm
    clear_screen()
    show_header("Confirmar Cambios")
    
    print("\nResumen de cambios:")
    print("-" * 50)
    for key in ['nombres', 'apellidos', 'fecha_nacimiento', 'fecha_defuncion', 
                'lugar_nacimiento', 'lugar_defuncion', 'sexo']:
        if key in person or key in updated_data:
            old_val = str(person.get(key, 'No especificado'))
            new_val = str(updated_data.get(key, 'No especificado'))
            if old_val != new_val:
                print(f"{key.capitalize().replace('_', ' ')}: {old_val} → {new_val}")
    
    if 'biografia' in updated_data and updated_data['biografia'] != person.get('biografia'):
        print("\nBiografía modificada (mostrando primeras 50 caracteres):")
        print(f"Antes: {str(person.get('biografia', 'No especificada'))[:50]}...")
        print(f"Ahora: {updated_data['biografia'][:50]}...")
    
    confirm = input("\n¿Desea guardar los cambios? (s/n): ").strip().lower()
    if confirm != 's':
        show_message("Cambios descartados.", "info")
        return False
    
    # Update the person
    success = edit_person(person['id_persona'], updated_data, user_id)
    if success:
        show_message("✅ Cambios guardados exitosamente.", "success")
        # Update the original person dictionary
        person.update(updated_data)
        return True
    else:
        show_message("❌ Error al guardar los cambios. Intente nuevamente.", "error")
        return False
