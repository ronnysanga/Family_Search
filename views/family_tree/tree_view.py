from typing import Dict, Any
from services.tree import print_family_tree
from utils.console_utils import show_header, get_input, clear_screen
from ..person.search_views import search_and_select_person

def show_family_tree_view():
    """Show interface to view a family tree"""
    while True:
        clear_screen()
        show_header("Ver Árbol Genealógico")
        
        # Buscar persona raíz
        print("Seleccione la persona para ver su árbol genealógico:")
        person = search_and_select_person("Buscar persona")
        if not person:
            return
            
        # Obtener profundidad máxima
        while True:
            try:
                depth = input("\nProfundidad del árbol (1-5, predeterminado 3): ").strip()
                if not depth:
                    depth = 3
                    break
                depth = int(depth)
                if 1 <= depth <= 5:
                    break
                print("La profundidad debe estar entre 1 y 5.")
            except ValueError:
                print("Por favor ingrese un número válido.")
        
        # Mostrar árbol
        clear_screen()
        show_header(f"Árbol Genealógico de {person['nombres']} {person['apellidos']}")
        print("-" * 80)
        print_family_tree(person['id_persona'], depth)
        print("\n" + "-" * 80)
        
        # Opciones adicionales
        print("\nOpciones:")
        print("1. Ver otra persona")
        print("2. Ver detalles de una persona")
        print("0. Volver al menú principal")
        
        option = get_input("\nSeleccione una opción: ")
        
        if option == '0':
            return
        elif option == '2':
            # Mostrar detalles de una persona específica
            from .person_details import show_person_details
            person_id = get_input("\nIngrese el ID de la persona: ")
            if person_id:
                show_person_details(person_id)
