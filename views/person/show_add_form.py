from typing import Dict, Any, Optional
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.person import add_person

def show_add_form(user_id: int) -> Optional[int]:
    clear_screen()
    show_header("Agregar Nueva Persona")
    
    print("\nComplete los datos de la persona. Los campos marcados con * son obligatorios.")
    
    person_data = {
        'nombres': get_input("* Nombres: ", required=True),
        'apellidos': get_input("* Apellidos: ", required=True)
    }
    
    print("\n--- INFORMACIÓN PERSONAL ---")
    
    print("\nFechas importantes:")
    print("  Fecha de nacimiento (opcional - formato YYYY-MM-DD): ", end='')
    fecha_nac = input().strip()
    if fecha_nac:
        person_data['fecha_nacimiento'] = fecha_nac
        
    print("  Fecha de fallecimiento (opcional - formato YYYY-MM-DD): ", end='')
    fecha_def = input().strip()
    if fecha_def:
        person_data['fecha_defuncion'] = fecha_def
    
    print("\nLugares:")
    print("  Lugar de nacimiento (opcional): ", end='')
    lugar_nac = input().strip()
    if lugar_nac:
        person_data['lugar_nacimiento'] = lugar_nac
    
    print("\nSexo (opcional):")
    print("  1. Masculino")
    print("  2. Femenino")
    print("  3. No especificar")
    print("  Opción (1-3, ENTER para omitir): ", end='')
    opcion = input().strip()
    
    if opcion == '1':
        person_data['sexo'] = 'masculino'
    elif opcion == '2':
        person_data['sexo'] = 'femenino'
    elif opcion and opcion != '3':  
        show_message("Opción no válida. Se omitirá el campo de sexo.", "advertencia")
    
    
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
    
    person_id = add_person(person_data, user_id)
    if person_id:
        show_message(f"✅ Persona agregada exitosamente con ID: {person_id}", "success")
        
        if input("\n¿Desea agregar relaciones familiares ahora? (s/n): ").lower() == 's':
            from ..family_tree.show_add_relationship import show_add_relationship
            show_add_relationship(user_id)
            
        return person_id
    else:
        show_message("❌ Error al guardar la persona. Intente nuevamente.", "error")
        return None
