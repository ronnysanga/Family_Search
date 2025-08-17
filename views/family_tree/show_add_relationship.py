from typing import Optional, Dict, Any
from utils.console_utils import show_header, show_message, get_input
from services.relationship import add_relationship
from ..person.select_person import select_person

def show_add_relationship(user_id: int) -> None:
    """
    Display interface for adding a family relationship between two people.
    
    Args:
        user_id: ID of the currently logged-in user
    """
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
            
        # Select relationship type
        relationship_type = _select_relationship_type()
        if not relationship_type:
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

def _select_relationship_type() -> Optional[Dict[str, str]]:
    """Display relationship type selection menu."""
    relationship_types = [
        ('1', 'Padre', 'padre', 'hijo(a)'),
        ('2', 'Madre', 'madre', 'hijo(a)'),
        ('3', 'Hijo', 'hijo', 'padre'),
        ('4', 'Hija', 'hija', 'madre'),
        ('5', 'Esposo', 'esposo', 'esposa'),
        ('6', 'Esposa', 'esposa', 'esposo'),
        ('7', 'Hermano', 'hermano', 'hermano(a)'),
        ('8', 'Hermana', 'hermana', 'hermano(a)')
    ]
    
    print("\nSeleccione el tipo de relación:")
    print("-" * 50)
    for code, label, _, _ in relationship_types:
        print(f"{code}. {label}")
    print("0. Cancelar")
    
    while True:
        choice = get_input("\nOpción: ").strip()
        if choice == '0':
            return None
            
        for rel in relationship_types:
            if rel[0] == choice:
                return {
                    'code': rel[0],
                    'label': rel[1],
                    'type': rel[2],
                    'inverse': rel[3]
                }
                
        show_message("Opción no válida. Intente nuevamente.", "error")

def _confirm_and_save_relationship(
    person1: Dict[str, Any], 
    person2: Dict[str, Any], 
    rel_type: Dict[str, str],
    user_id: int
) -> None:
    """
    Confirm and save a relationship between two people.
    
    Args:
        person1: First person in the relationship
        person2: Second person in the relationship
        rel_type: Relationship type information
        user_id: ID of the user creating the relationship
    """
    # Show confirmation
    print(f"\nConfirmar relación:")
    print(f"{person1['nombres']} {person1['apellidos']} es {rel_type['label'].lower()} de {person2['nombres']} {person2['apellidos']}")
    
    confirm = input("\n¿Confirmar? (s/n): ").strip().lower()
    if confirm != 's':
        return
    
    # Save relationship in both directions
    success1 = add_relationship(
        person1['id_persona'],
        person2['id_persona'],
        rel_type['type'],
        user_id
    )
    
    success2 = add_relationship(
        person2['id_persona'],
        person1['id_persona'],
        rel_type['inverse'],
        user_id
    )
    
    if success1 and success2:
        show_message("✅ Relación familiar establecida exitosamente.", "success")
    else:
        show_message("❌ Error al establecer la relación. Intente nuevamente.", "error")
