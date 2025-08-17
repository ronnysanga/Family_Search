from typing import Dict, Any, Optional
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.person import add_person

def show_add_form(user_id: int) -> Optional[int]:
    clear_screen()
    show_header("Agregar Nueva Persona")
    
    print("\nComplete los datos de la persona. Los campos marcados con * son obligatorios.")
    
    # Collect person data
    person_data = {
        'nombres': get_input("* Nombres: ", required=True),
        'apellidos': get_input("* Apellidos: ", required=True),
        'fecha_nacimiento': get_input("  Fecha de nacimiento (YYYY-MM-DD): "),
        'fecha_defuncion': get_input("  Fecha de fallecimiento (YYYY-MM-DD, opcional): "),
        'lugar_nacimiento': get_input("  Lugar de nacimiento (opcional): "),
        'lugar_defuncion': get_input("  Lugar de fallecimiento (opcional): "),
        'biografia': get_input("  Biografía (opcional): ", multiline=True)
    }
    
    # Handle sex input with validation
    while True:
        print("\nOpciones de sexo:")
        print("1. Masculino")
        print("2. Femenino")
        opcion = get_input("Seleccione una opción (1-2): ").strip()
        if opcion == '1':
            person_data['sexo'] = 'masculino'
        elif opcion == '2':
            person_data['sexo'] = 'femenino'
        else:
            show_message("Opción no válida. Debe seleccionar 1 o 2.", "error")
            continue
    
    # Show confirmation
    clear_screen()
    show_header("Confirmar Datos")
    
    print("\nRevise los datos ingresados:")
    print("-" * 50)
    for key, value in person_data.items():
        if value:  # Only show fields with values
            print(f"{key.capitalize().replace('_', ' ')}: {value}")
    
    confirm = input("\n¿Desea guardar esta persona? (s/n): ").strip().lower()
    if confirm != 's':
        show_message("Operación cancelada.", "info")
        return None
    
    # Create the person
    person_id = add_person(person_data, user_id)
    if person_id:
        show_message(f"✅ Persona agregada exitosamente con ID: {person_id}", "success")
        
        # Ask if user wants to add relationships
        if input("\n¿Desea agregar relaciones familiares ahora? (s/n): ").lower() == 's':
            from ..family_tree.show_add_relationship import show_add_relationship
            show_add_relationship(user_id)
            
        return person_id
    else:
        show_message("❌ Error al guardar la persona. Intente nuevamente.", "error")
        return None
