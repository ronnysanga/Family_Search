from typing import Dict, Optional, List, Any
from utils.console_utils import clear_screen, show_message, get_input
from services.relationship.add import add_relationship as add_rel
from services.person.get import get_person_by_id
from ..person.select_person import select_person

def get_person_gender(person_id: int) -> Optional[str]:
    """Obtiene el género de una persona desde la base de datos"""
    person = get_person_by_id(person_id)
    return person.get('sexo') if person else None

def show_add_relationship(user_id: int, person1_id: Optional[int] = None) -> None:
    """
    Muestra la interfaz para agregar una relación familiar.
    """
    clear_screen()
    print("\n=== AGREGAR RELACIÓN FAMILIAR ===\n")
    
    # Seleccionar la primera persona si no se proporciona
    if not person1_id:
        person1 = select_person("Seleccione la primera persona")
        if not person1:
            return
        person1_id = person1['id_persona']
    
    # Seleccionar la segunda persona
    person2 = select_person("Seleccione la persona relacionada")
    if not person2:
        return
    
    if person1_id == person2['id_persona']:
        show_message("No puede seleccionar la misma persona dos veces.", "error")
        input("\nPresione ENTER para continuar...")
        return
    
    # Obtener géneros
    person1_gender = get_person_gender(person1_id)
    person2_gender = get_person_gender(person2['id_persona'])
    
    # Seleccionar el tipo de relación
    print("\nTipo de relación:")
    print("1. Padre/Madre")
    print("2. Hijo/Hija")
    print("3. Cónyuge")
    print("4. Hermano/Hermana")
    
    rel_choice = get_input("\nSeleccione el tipo de relación (1-4): ")
    
    # Mapear opción a tipo de relación
    rel_type_map = {
        '1': 'padre',
        '2': 'hijo',
        '3': 'esposo',
        '4': 'hermano'
    }
    
    if rel_choice not in rel_type_map:
        show_message("Opción no válida", "error")
        return
    
    base_rel_type = rel_type_map[rel_choice]
    
    # Determinar el tipo de relación basado en el género
    if base_rel_type == 'padre':
        rel_type = 'madre' if person1_gender == 'femenino' else 'padre'
    elif base_rel_type == 'hijo':
        rel_type = 'hija' if person1_gender == 'femenino' else 'hijo'
    elif base_rel_type == 'esposo':
        rel_type = 'esposa' if person1_gender == 'femenino' else 'esposo'
    elif base_rel_type == 'hermano':
        rel_type = 'hermana' if person1_gender == 'femenino' else 'hermano'
    
    # Agregar la relación
    try:
        success = add_rel(
            person1_id=person1_id,
            person2_id=person2['id_persona'],
            relationship_type=rel_type,
            user_id=user_id
        )
        
        # Agregar relación inversa si es necesario
        if success and rel_type in ['padre', 'madre']:
            inverse_rel = 'hijo' if person2_gender == 'masculino' else 'hija'
            add_rel(
                person1_id=person2['id_persona'],
                person2_id=person1_id,
                relationship_type=inverse_rel,
                user_id=user_id
            )
        elif success and rel_type in ['hijo', 'hija']:
            inverse_rel = 'padre' if person2_gender == 'masculino' else 'madre'
            add_rel(
                person1_id=person2['id_persona'],
                person2_id=person1_id,
                relationship_type=inverse_rel,
                user_id=user_id
            )
        
        if success:
            show_message("Relación agregada exitosamente", "success")
        else:
            show_message("No se pudo agregar la relación", "error")
            
    except Exception as e:
        show_message(f"Error al agregar la relación: {str(e)}", "error")
    
    input("\nPresione ENTER para continuar...")
