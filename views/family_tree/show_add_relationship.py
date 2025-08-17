from typing import Optional, Dict, Any
from utils.console_utils import show_header, show_message, get_input
from services.relationship import add_relationship
from ..person.select_person import select_person

def show_add_relationship(user_id: int) -> None:
    show_header("Agregar Relación Familiar")
    
    # Select first person
    print("Seleccione la primera persona:")
    person1 = select_person()
    if not person1:
        return
    
    while True:
        show_header(f"Agregar Familiar para {person1['nombres']} {person1['apellidos']}")
        
        # Select second person
        print(f"\nSeleccione el familiar para {person1['nombres']}:")
        person2 = select_person()
        if not person2:
            if input("\n¿Desea seleccionar otra primera persona? (s/n): ").lower() != 's':
                return
            continue
            
        if person1['id_persona'] == person2['id_persona']:
            show_message("No puede seleccionar la misma persona dos veces.", "error")
            input("Presione Enter para continuar...")
            continue
            
        # Select relationship type based on persons' genders
        relationship_type = _select_relationship_type(person1, person2)
        if not relationship_type:
            if input("\n¿Desea seleccionar otra primera persona? (s/n): ").lower() == 's':
                break
            continue
            
        # Confirm and save
        _confirm_and_save_relationship(
            person1, 
            person2, 
            relationship_type, 
            user_id
        )
        
        if input("\n¿Desea agregar otra relación? (s/n): ").lower() != 's':
            break

def _select_relationship_type(person1: Dict[str, Any], person2: Dict[str, Any]) -> Optional[Dict[str, str]]:
    gender1 = person1.get('sexo', '').lower()
    gender2 = person2.get('sexo', '').lower()
    
    # Define all possible relationship types with their conditions
    relationship_types = [
        # Parent relationships
        {'code': '1', 'type': 'padre', 'label': 'Padre', 
         'inverse': 'hijo', 'gender': 'masculino', 'inverse_gender': None},
        {'code': '2', 'type': 'madre', 'label': 'Madre', 
         'inverse': 'hijo', 'gender': 'femenino', 'inverse_gender': None},
         
        # Child relationships
        {'code': '3', 'type': 'hijo', 'label': 'Hijo', 
         'inverse': 'padre', 'gender': 'masculino', 'inverse_gender': None},
        {'code': '4', 'type': 'hijo', 'label': 'Hijo', 
         'inverse': 'madre', 'gender': 'masculino', 'inverse_gender': None},
        {'code': '5', 'type': 'hija', 'label': 'Hija', 
         'inverse': 'padre', 'gender': 'femenino', 'inverse_gender': None},
        {'code': '6', 'type': 'hija', 'label': 'Hija', 
         'inverse': 'madre', 'gender': 'femenino', 'inverse_gender': None},
         
        # Spouse relationships
        {'code': '7', 'type': 'esposo', 'label': 'Esposo', 
         'inverse': 'esposa', 'gender': 'masculino', 'inverse_gender': 'femenino'},
        {'code': '8', 'type': 'esposa', 'label': 'Esposa', 
         'inverse': 'esposo', 'gender': 'femenino', 'inverse_gender': 'masculino'},
         
        # Sibling relationships
        {'code': '9', 'type': 'hermano', 'label': 'Hermano', 
         'inverse': 'hermano', 'gender': 'masculino', 'inverse_gender': None},
        {'code': '10', 'type': 'hermano', 'label': 'Hermano', 
         'inverse': 'hermana', 'gender': 'masculino', 'inverse_gender': 'femenino'},
        {'code': '11', 'type': 'hermana', 'label': 'Hermana', 
         'inverse': 'hermano', 'gender': 'femenino', 'inverse_gender': 'masculino'},
        {'code': '12', 'type': 'hermana', 'label': 'Hermana', 
         'inverse': 'hermana', 'gender': 'femenino', 'inverse_gender': 'femenino'}
    ]
    
    # Filter valid relationship options based on genders
    valid_relationships = []
    option_number = 1
    
    for rel in relationship_types:
        # Check if the relationship is valid given the persons' genders
        gender_match = (not rel['gender'] or gender1 == rel['gender'])
        inverse_gender_match = (not rel['inverse_gender'] or gender2 == rel['inverse_gender'])
        
        if gender_match and inverse_gender_match:
            valid_relationships.append({
                'code': str(option_number),
                'label': rel['label'],
                'type': rel['type'],
                'inverse': rel['inverse'],
                'gender_specific': bool(rel['gender'])
            })
            option_number += 1
    
    if not valid_relationships:
        show_message("No hay tipos de relación válidos disponibles para estas personas.", "error")
        return None
    
    # Display available relationship options
    print("\nSeleccione el tipo de relación:")
    print("-" * 50)
    for rel in valid_relationships:
        print(f"{rel['code']}. {rel['label']}")
    print("0. Cancelar")
    
    while True:
        choice = get_input("\nOpción: ").strip()
        if choice == '0':
            return None
            
        for rel in valid_relationships:
            if rel['code'] == choice:
                return rel
                
        show_message("Opción no válida. Intente nuevamente.", "error")

def _confirm_and_save_relationship(
    person1: Dict[str, Any], 
    person2: Dict[str, Any], 
    rel_type: Dict[str, str],
    user_id: int
) -> None:
    print("\nConfirmar relación:")
    print(f"{person1['nombres']} {person1['apellidos']} es {rel_type['label'].lower()} de {person2['nombres']} {person2['apellidos']}")
    
    confirm = input("\n¿Confirmar? (s/n): ").strip().lower()
    if confirm != 's':
        return
    
    try:
        # Save relationship in both directions
        success1 = add_relationship(
            person1['id_persona'],
            person2['id_persona'],
            rel_type['type'],
            user_id
        )
        
        # For the inverse relationship, we need to determine the correct type based on person1's gender
        inverse_relationship = rel_type['inverse']
        
        # Special handling for parent-child relationships
        if rel_type['type'] in ['padre', 'madre']:
            # If person1 is parent, person2 must be child (hijo/hija based on gender)
            child_gender = person2.get('sexo', '').lower()
            inverse_relationship = 'hijo' if child_gender == 'masculino' else 'hija'
        elif rel_type['type'] in ['hijo', 'hija']:
            # If person1 is child, person2 must be parent (padre/madre based on gender)
            parent_gender = person2.get('sexo', '').lower()
            inverse_relationship = 'padre' if parent_gender == 'masculino' else 'madre'
        
        success2 = add_relationship(
            person2['id_persona'],
            person1['id_persona'],
            inverse_relationship,
            user_id
        )
        
        if success1 and success2:
            show_message("✅ Relación familiar establecida exitosamente.", "success")
            
            # Log the relationship creation
            from datetime import datetime
            print(f"\nRegistro de relación creado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
            print(f"- {person1['nombres']} {person1['apellidos']} es {rel_type['label'].lower()} de {person2['nombres']} {person2['apellidos']}")
            print(f"- {person2['nombres']} {person2['apellidos']} es {inverse_relationship} de {person1['nombres']} {person1['apellidos']}")
        else:
            show_message("❌ Error al establecer la relación. Intente nuevamente.", "error")
            
    except Exception as e:
        show_message(f"❌ Error inesperado: {str(e)}", "error")
