from services.family_tree.relationship_service import add_relationship
from services.person import get_person_by_id
from utils.console_utils import show_header, show_message, get_input, clear_screen
from ..person.search_views import search_and_select_person

def show_add_relationship(user_id: int):
    while True:
        clear_screen()
        show_header("Agregar Relación Familiar")
        
        # Buscar primera persona
        print("Seleccione la primera persona:")
        person1 = search_and_select_person("Buscar primera persona")
        if not person1:
            return
            
        # Buscar segunda persona
        print("\nSeleccione la segunda persona:")
        person2 = search_and_select_person("Buscar segunda persona")
        if not person2:
            return
            
        if person1['id_persona'] == person2['id_persona']:
            show_message("No puede seleccionar la misma persona dos veces.", "error")
            input("Presione Enter para continuar...")
            continue
            
        # Mostrar tipos de relación disponibles
        show_header(f"Relación entre {person1['nombres']} y {person2['nombres']}")
        print("Tipos de relación disponibles:")
        print("1. Padre/Madre")
        print("2. Hijo/Hija")
        print("3. Esposo/Esposa")
        print("4. Hermano/Hermana")
        
        # Obtener tipo de relación
        while True:
            rel_type = get_input("\nSeleccione el tipo de relación (1-4, 0 para cancelar): ")
            if rel_type == '0':
                return
                
            if rel_type not in ['1', '2', '3', '4']:
                show_message("Opción no válida. Intente nuevamente.", "error")
                continue
                
            # Mapear opción a tipo de relación
            rel_types = {
                '1': 'parent',
                '2': 'child',
                '3': 'spouse',
                '4': 'sibling'
            }
            
            # Agregar la relación
            success = add_relationship(
                person1['id_persona'],
                person2['id_persona'],
                rel_types[rel_type],
                user_id
            )
            
            if success:
                show_message("Relación agregada exitosamente.", "success")
            else:
                show_message("No se pudo agregar la relación.", "error")
                
            input("\nPresione Enter para continuar...")
            break
