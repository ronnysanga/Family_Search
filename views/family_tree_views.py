"""
Family Tree Views Module

This module provides the user interface for managing and visualizing family trees.
"""
from typing import Dict, List, Optional, Callable, Any
from services.family_tree_service import (
    create_person, search_people, get_person_by_id,
    add_relationship, print_family_tree, get_relationships
)
from utils.console_utils import (
    show_header, show_message, get_input,
    clear_screen, show_menu
)

def show_create_person(user_id: int) -> Optional[int]:
    """Show form to create a new person"""
    show_header("Agregar Nueva Persona al Árbol Genealógico")
    
    person_data = {
        'nombres': get_input("Nombres: ", required=True),
        'apellidos': get_input("Apellidos: ", required=True),
        'fecha_nacimiento': get_input("Fecha de nacimiento (YYYY-MM-DD, opcional): "),
        'fecha_defuncion': get_input("Fecha de defunción (YYYY-MM-DD, opcional): "),
        'sexo': get_input("Sexo (M/F, opcional): ").upper(),
        'lugar_nacimiento': get_input("Lugar de nacimiento (opcional): "),
        'lugar_defuncion': get_input("Lugar de defunción (opcional): "),
        'biografia': get_input("Biografía (opcional): ")
    }
    
    # Clean empty strings
    person_data = {k: v if v else None for k, v in person_data.items()}
    
    # Validate sex
    if person_data['sexo'] and person_data['sexo'] not in ['M', 'F']:
        show_message("El sexo debe ser 'M' o 'F'.", "error")
        return None
    
    person_id = create_person(person_data, user_id)
    if person_id:
        show_message(f"✅ Persona agregada con ID: {person_id}", "success")
        return person_id
    return None

def search_and_select_person(prompt: str = "Buscar persona") -> Optional[Dict]:
    """Search for a person and allow selection from results"""
    while True:
        search_term = get_input(f"{prompt} (o 'salir' para cancelar): ")
        if search_term.lower() == 'salir':
            return None
            
        results = search_people(search_term)
        if not results:
            show_message("No se encontraron personas con ese criterio.", "warning")
            continue
            
        # Show search results
        show_header("Resultados de Búsqueda")
        for i, person in enumerate(results, 1):
            print(f"{i}. {person['nombres']} {person['apellidos']}")
            print(f"   Fecha de nacimiento: {person.get('fecha_nac', 'No especificada')}")
            print(f"   ID: {person['id_persona']}")
            print("-" * 40)
            
        # Let user select a person
        while True:
            selection = get_input("\nSeleccione un número o '0' para buscar de nuevo: ")
            if selection == '0':
                break
                
            try:
                idx = int(selection) - 1
                if 0 <= idx < len(results):
                    return results[idx]
                print("Número fuera de rango. Intente nuevamente.")
            except ValueError:
                print("Por favor ingrese un número válido.")

def show_add_relationship(user_id: int):
    """Show interface to add a family relationship"""
    show_header("Agregar Relación Familiar")
    
    # Get first person
    print("\nSeleccione la primera persona:")
    person1 = search_and_select_person()
    if not person1:
        return
        
    # Get second person (the one to relate to the first)
    print(f"\nSeleccione la persona que es familiar de {person1['nombres']} {person1['apellidos']}:")
    person2 = search_and_select_person()
    if not person2:
        return
        
    # Select relationship type
    relationship_types = {
        '1': ('padre', 'hijo'),
        '2': ('madre', 'hijo'),
        '3': ('hijo', 'padre'),
        '4': ('hija', 'madre'),
        '5': ('esposo', 'esposa'),
        '6': ('esposa', 'esposo'),
        '7': ('hermano', 'hermano'),
        '8': ('hermana', 'hermana')
    }
    
    show_header("Seleccionar Tipo de Relación")
    print("\n¿Cuál es la relación entre las personas?")
    print("1. Padre")
    print("2. Madre")
    print("3. Hijo")
    print("4. Hija")
    print("5. Esposo")
    print("6. Esposa")
    print("7. Hermano")
    print("8. Hermana")
    
    while True:
        choice = get_input("\nSeleccione una opción: ")
        if choice in relationship_types:
            rel_type, inverse_type = relationship_types[choice]
            break
        print("Opción inválida. Intente nuevamente.")
    
    # Add the relationship in both directions
    success1 = add_relationship(
        person1['id_persona'], person2['id_persona'], rel_type, user_id
    )
    
    # Add the inverse relationship
    success2 = add_relationship(
        person2['id_persona'], person1['id_persona'], inverse_type, user_id
    )
    
    if success1 and success2:
        show_message("✅ Relación familiar establecida exitosamente.", "success")
    else:
        show_message("No se pudo establecer la relación completa.", "warning")

def show_family_tree():
    """Show interface to view a family tree"""
    show_header("Ver Árbol Genealógico")
    
    # Let user select the root person
    print("Seleccione la persona raíz del árbol:")
    person = search_and_select_person()
    if not person:
        return
        
    # Get tree depth
    while True:
        try:
            depth = get_input("Profundidad del árbol (1-5, predeterminado 3): ")
            if not depth:
                depth = 3
                break
            depth = int(depth)
            if 1 <= depth <= 5:
                break
            print("La profundidad debe estar entre 1 y 5.")
        except ValueError:
            print("Por favor ingrese un número válido.")
    
    # Generate and display the tree
    clear_screen()
    show_header(f"Árbol Genealógico de {person['nombres']} {person['apellidos']}")
    print("\n" + "=" * 50 + "\n")
    
    print_family_tree(person['id_persona'], depth)
    
    print("\n" + "=" * 50)
    input("\nPresione Enter para continuar...")

def show_family_tree_menu(user_id: int):
    """Show the main family tree management menu"""
    while True:
        clear_screen()
        show_header("Árbol Genealógico")
        
        menu_options = [
            ("Agregar nueva persona", lambda: show_create_person(user_id)),
            ("Buscar persona", lambda: search_and_select_person() and None),
            ("Agregar relación familiar", lambda: show_add_relationship(user_id)),
            ("Ver árbol genealógico", show_family_tree),
            ("Volver al menú principal", None)
        ]
        
        # Mostrar opciones
        for i, (text, _) in enumerate(menu_options, 1):
            print(f"{i}. {text}")
        
        # Obtener selección del usuario
        try:
            choice = get_input("\nSeleccione una opción: ")
            if not choice:
                continue
                
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(menu_options):
                if choice_idx == len(menu_options) - 1:  # Última opción (Salir)
                    break
                
                # Ejecutar la función correspondiente
                func = menu_options[choice_idx][1]
                if func:
                    func()
                    input("\nPresione Enter para continuar...")
            else:
                show_message("Opción no válida. Intente nuevamente.", "error")
                
        except ValueError:
            show_message("Por favor ingrese un número válido.", "error")
