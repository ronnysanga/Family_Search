from typing import Dict, Any, Optional
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.person.update import edit_person

def get_sexo_display(sexo: Optional[str]) -> str:
    """Convert sexo value to display format
    
    Args:
        sexo: The gender value from the database (can be None, 'm', 'f', 'masculino', 'femenino')
        
    Returns:
        Formatted gender string for display
    """
    if not sexo:
        return 'No especificado'
        
    sexo = str(sexo).lower().strip()
    
    if sexo in ['m', 'masculino']:
        return 'Masculino'
    elif sexo in ['f', 'femenino']:
        return 'Femenino'
        
    return sexo.capitalize()

def show_edit_form(person: Dict[str, Any], user_id: int) -> bool:
    updated_data = person.copy()
    changes_made = False
    
    while True:
        clear_screen()
        show_header(f"EDITAR PERFIL DE {person['nombres'].upper()}")
        
        print("\nSeleccione una opción:")
        print(f" 1. Nombres: {updated_data.get('nombres', '')}")
        print(f" 2. Apellidos: {updated_data.get('apellidos', '')}")
        print(f" 3. Fecha de Nacimiento: {updated_data.get('fecha_nacimiento', 'No especificada')}")
        print(f" 4. Fecha de Fallecimiento: {updated_data.get('fecha_defuncion', 'No especificada')}")
        print(f" 5. Lugar de Nacimiento: {updated_data.get('lugar_nacimiento', 'No especificado')}")
        print(f" 6. Lugar de Fallecimiento: {updated_data.get('lugar_defuncion', 'No especificado')}")
        print(f" 7. Sexo: {get_sexo_display(updated_data.get('sexo'))}")
        
        print("\n 0. Salir sin guardar cambios")
        
        field_choice = get_input("\nOpción (0-7): ").strip()
        
        if field_choice == '0':
            if changes_made and not get_yes_no_input("¿Está seguro que desea salir sin guardar los cambios? (s/n): "):
                continue
            return False
        
        if not field_choice:  
            if changes_made:
                if confirm_changes(person, updated_data, user_id):
                    return True
                changes_made = False
                continue
            return False
            
        field_info = {
            '1': {'name': 'nombres', 'display': 'Nombres'},
            '2': {'name': 'apellidos', 'display': 'Apellidos'},
            '3': {'name': 'fecha_nacimiento', 'display': 'Fecha de Nacimiento'},
            '4': {'name': 'fecha_defuncion', 'display': 'Fecha de Fallecimiento'},
            '5': {'name': 'lugar_nacimiento', 'display': 'Lugar de Nacimiento'},
            '6': {'name': 'lugar_defuncion', 'display': 'Lugar de Fallecimiento'},
            '7': {'name': 'sexo', 'display': 'Sexo'},
            '8': {'name': 'biografia', 'display': 'Biografía'}
        }
        
        if field_choice not in field_info:
            show_message("❌ Opción no válida. Intente nuevamente.", "error")
            input("\nPresione ENTER para continuar...")
            continue
            
        field_name = field_info[field_choice]['name']
        field_display = field_info[field_choice]['display']
        current_value = updated_data.get(field_name, '')
        
        if field_name == 'sexo':
            new_value = get_sexo_input(current_value)
        elif field_name == 'biografia':
            new_value = get_biografia_input(current_value)
        else:
            prompt = f"\n{field_display} (actual: {current_value if current_value else 'No especificado'})"
            prompt += "\nNuevo valor (presione ENTER para cancelar): "
            new_value = get_input(prompt).strip()
        
        if new_value is not None and new_value != current_value:
            if confirm_field_change(field_display, current_value, new_value):
                updated_data[field_name] = new_value
                changes_made = True
                show_message("✅ Cambio registrado.", "success")
            
            if not get_yes_no_input("\n¿Desea editar otro campo? (s/n): "):
                if changes_made:
                    return confirm_changes(person, updated_data, user_id)
                return False
        elif new_value is not None: 
            show_message("No se realizaron cambios.", "info")
            input("\nPresione ENTER para continuar...")

def get_sexo_input(current_value: str) -> str:
    """Get gender input from user
    
    Returns:
        str: 'masculino' or 'femenino' based on user selection
    """
    while True:
        current_display = get_sexo_display(current_value)
        print("\nOpciones de sexo (solo se permiten 'masculino' o 'femenino'):")
        print(f"1. Masculino{' (actual)' if current_display == 'Masculino' else ''}")
        print(f"2. Femenino{' (actual)' if current_display == 'Femenino' else ''}")
        print("3. Cancelar")
        
        opcion = get_input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == '1':
            return 'masculino'
        elif opcion == '2':
            return 'femenino'
        elif opcion == '3':
            return current_value
        
        show_message("❌ Opción no válida. Por favor seleccione 1, 2 o 3.", "error")

def get_biografia_input(current_value: str) -> str:
    """Get biography input from user"""
    print("\nBiografía actual (presione ENTER para mantenerla igual):")
    if current_value:
        print("-" * 50)
        print(current_value)
        print("-" * 50)
    else:
        print("No especificada")
    
    print("\nIngrese la nueva biografía (presione ENTER dos veces para terminar):")
    try:
        lines = []
        while True:
            line = input()
            if not line and lines and not lines[-1]:
                lines.pop() 
                break
            lines.append(line)
    except EOFError:
        pass
    
    new_biography = '\n'.join(lines).strip()
    return new_biography if new_biography else current_value

def confirm_field_change(field_name: str, old_value: str, new_value: str) -> bool:
    """Ask for confirmation before changing a field"""
    print("\nConfirmar cambio:")
    print(f"Campo: {field_name}")
    print(f"Valor actual: {old_value if old_value else 'No especificado'}")
    print(f"Nuevo valor: {new_value if new_value else 'No especificado'}")
    return get_yes_no_input("\n¿Desea guardar este cambio? (s/n): ")

def confirm_changes(person: Dict[str, Any], updated_data: Dict[str, Any], user_id: int) -> bool:
    """Show all changes and confirm before saving"""
    clear_screen()
    show_header("CONFIRMAR CAMBIOS")
    
    changes = []
    for key in ['nombres', 'apellidos', 'fecha_nacimiento', 'fecha_defuncion', 
                'lugar_nacimiento', 'lugar_defuncion', 'sexo']:
        if key in person or key in updated_data:
            old_val = person.get(key, '')
            new_val = updated_data.get(key, '')
            if old_val != new_val:
                changes.append({
                    'field': key.replace('_', ' ').title(),
                    'old': old_val if old_val else 'No especificado',
                    'new': new_val if new_val else 'No especificado'
                })
    
    if 'biografia' in updated_data and updated_data['biografia'] != person.get('biografia'):
        old_bio = person.get('biografia', '')
        new_bio = updated_data.get('biografia', '')
        changes.append({
            'field': 'Biografía',
            'old': old_bio[:50] + ('...' if len(old_bio) > 50 else ''),
            'new': new_bio[:50] + ('...' if len(new_bio) > 50 else '')
        })
    
    if not changes:
        show_message("No se realizaron cambios.", "info")
        return False
    
    print("\nResumen de cambios:")
    print("-" * 80)
    print(f"{'CAMPO':<25} | {'VALOR ANTERIOR':<25} | {'NUEVO VALOR'}")
    print("-" * 80)
    for change in changes:
        print(f"{change['field']:<25} | {str(change['old'])[:25]:<25} | {str(change['new'])[:25]}")
    
    if not get_yes_no_input("\n¿Desea guardar los cambios? (s/n): "):
        show_message("❌ Cambios descartados.", "warning")
        return False
    
    success = edit_person(person['id_persona'], updated_data, user_id)
    if success:
        show_message("✅ Cambios guardados exitosamente.", "success")
        person.update(updated_data)
        input("\nPresione ENTER para continuar...")
        return True
    else:
        show_message("❌ Error al guardar los cambios. Intente nuevamente.", "error")
        input("\nPresione ENTER para continuar...")
        return False

def get_yes_no_input(prompt: str) -> bool:
    """Get yes/no input from user"""
    while True:
        response = input(prompt).strip().lower()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Por favor responda 's' para sí o 'n' para no.")
