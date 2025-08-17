from typing import Optional
from utils.console_utils import show_header, get_input, show_message
from services.tree import print_family_tree
from ..person.select_person import select_person

def show_family_tree(person_id: Optional[int] = None) -> None:
    """
    Display interface for viewing a family tree.
    If person_id is provided, shows that person's family tree.
    Otherwise, allows selecting a person to view their family tree.
    
    Args:
        person_id: Optional ID of the person to show the family tree for
    """
    show_header("Ver Árbol Genealógico")
    
    if person_id is None:
        # Let user select the root person if not provided
        print("Seleccione la persona raíz del árbol:")
        person = select_person()
        if not person:
            return
    else:
        from services.person import get_person_by_id
        person = get_person_by_id(person_id)
        if not person:
            show_message("Persona no encontrada.", "error")
            return
        
    # Get tree depth
    while True:
        try:
            depth_input = get_input("Profundidad del árbol (1-5, predeterminado 3): ")
            depth = int(depth_input) if depth_input else 3
            if 1 <= depth <= 5:
                break
            show_message("La profundidad debe estar entre 1 y 5.", "error")
        except ValueError:
            show_message("Por favor ingrese un número válido.", "error")
    
    # Display the family tree
    show_header(f"Árbol Genealógico de {person['nombres']} {person['apellidos']}")
    print("\n" + "=" * 50 + "\n")
    
    print_family_tree(person['id_persona'], depth)
    
    print("\n" + "=" * 50)
    input("\nPresione Enter para continuar...")
