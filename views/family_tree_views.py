from typing import Dict, List, Optional, Callable, Any
from services.person.create import create_person
from services.person.search import search_people
from services.person import get_person_by_id
from services.relationship import add_relationship, get_relationships
from services.tree import print_family_tree
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
    """
    Busca una persona y permite seleccionarla de los resultados.
    
    Args:
        prompt: Texto a mostrar al pedir la búsqueda
        
    Returns:
        dict: Datos de la persona seleccionada o None si se cancela
    """
    while True:
        clear_screen()
        show_header("Búsqueda de Personas")
        print("\n" + "="*50)
        print(f"{prompt}".center(50))
        print("="*50)
        print("\nIngrese el nombre, apellido o parte de estos.")
        print("Presione ENTER sin escribir para ver todas las personas.")
        print("Escriba 'salir' para cancelar.")
        
        search_term = input("\n🔍 Búsqueda: ").strip()
        
        if search_term.lower() == 'salir':
            return None
            
        # Si no hay término de búsqueda, obtener todas las personas
        results = search_people(search_term) if search_term else search_people("")
        
        if not results:
            print("\n" + "-"*50)
            print("No se encontraron personas que coincidan con la búsqueda.")
            input("\nPresione ENTER para intentar de nuevo...")
            continue
            
        # Mostrar resultados de forma más clara
        while True:
            clear_screen()
            show_header("Resultados de Búsqueda")
            print(f"Se encontraron {len(results)} personas:")
            print("-"*80)
            
            # Mostrar encabezado de la tabla
            print(f"{'#':<4} {'NOMBRES':<25} {'APELLIDOS':<25} {'NACIMIENTO':<12} {'SEXO':<6}")
            print("-"*80)
            
            # Mostrar cada resultado
            for i, person in enumerate(results, 1):
                nombres = person.get('nombres', '')[:20]
                apellidos = person.get('apellidos', '')[:20]
                fecha_nac = str(person.get('fecha_nacimiento', ''))[:10]
                sexo = person.get('sexo', '')[:1].upper()
                
                print(f"{i:<4} {nombres:<25} {apellidos:<25} {fecha_nac:<12} {sexo:<6}")
            
            # Opciones para el usuario
            print("\n" + "-"*80)
            print("INSTRUCCIONES:")
            print(f"- Ingrese un número del 1 al {len(results)} para seleccionar una persona")
            print("- Escriba 'buscar' para realizar una nueva búsqueda")
            print("- Escriba 'salir' para cancelar")
            
            choice = input("\nSu elección: ").strip().lower()
            
            if choice == 'salir':
                return None
            elif choice == 'buscar':
                break
            elif choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(results):
                    return results[index]
                
            # Si llegamos aquí, la opción no es válida
            print("\n❌ Opción no válida. Por favor intente de nuevo.")
            input("Presione ENTER para continuar...")

def show_add_relationship(user_id: int):
    """
    Muestra la interfaz para agregar una relación familiar entre dos personas.
    
    Args:
        user_id: ID del usuario que está realizando la acción
    """
    while True:
        clear_screen()
        show_header("AGREGAR RELACIÓN FAMILIAR")
        print("\n" + "="*50)
        print("PASO 1: Seleccione la primera persona".center(50))
        print("="*50)
        print("\nBusque y seleccione la primera persona de la relación:")
        
        person1 = search_and_select_person("Buscar primera persona")
        if not person1:
            return  # Usuario canceló
            
        while True:
            clear_screen()
            show_header("AGREGAR RELACIÓN FAMILIAR")
            print("\n" + "="*50)
            print(f"PRIMERA PERSONA: {person1['nombres']} {person1['apellidos']}".center(50))
            print("="*50)
            print("\nPASO 2: Seleccione la segunda persona")
            print(f"\nBusque y seleccione la persona que es familiar de {person1['nombres']} {person1['apellidos']}:")
            
            person2 = search_and_select_person(f"Buscar familiar de {person1['nombres']}")
            if not person2:
                if input("\n¿Desea seleccionar otra primera persona? (s/n): ").lower() == 's':
                    break
                else:
                    return  # Usuario canceló
                    
            if person1['id_persona'] == person2['id_persona']:
                show_message("No puede seleccionar la misma persona dos veces.", "error")
                input("Presione ENTER para continuar...")
                continue
                
            # Mostrar resumen de la relación a crear
            clear_screen()
            show_header("CONFIRMAR RELACIÓN")
            print("\n" + "="*70)
            print(f"Vamos a relacionar a:".center(70))
            print(f"{person1['nombres']} {person1['apellidos']} (ID: {person1['id_persona']})")
            print("con:")
            print(f"{person2['nombres']} {person2['apellidos']} (ID: {person2['id_persona']})")
            print("="*70)
            
            # Seleccionar tipo de relación
            relationship_types = [
                ('1', 'Padre', 'padre', 'hijo(a)'),
                ('2', 'Madre', 'madre', 'hijo(a)'),
                ('3', 'Hijo', 'hijo', 'padre'),
                ('4', 'Hija', 'hija', 'madre'),
                ('5', 'Esposo', 'esposo', 'esposa'),
                ('6', 'Esposa', 'esposa', 'esposo'),
                ('7', 'Hermano', 'hermano', 'hermano(a)'),
                ('8', 'Hermana', 'hermana', 'hermano(a)'),
                ('9', 'Abuelo', 'abuelo', 'nieto(a)'),
                ('10', 'Abuela', 'abuela', 'nieto(a)')
            ]
            
            print("\nSeleccione el tipo de relación:")
            print("-"*50)
            for code, label, _, _ in relationship_types:
                print(f"{code}. {label}")
            print("0. Cancelar")
            print("-"*50)
            
            while True:
                choice = input("\nOpción: ").strip()
                
                if choice == '0':
                    break
                    
                # Buscar la relación seleccionada
                selected_rel = None
                for rel in relationship_types:
                    if rel[0] == choice:
                        selected_rel = rel
                        break
                        
                if not selected_rel:
                    print("Opción inválida. Intente nuevamente.")
                    continue
                    
                # Mostrar confirmación
                _, label, rel_type, inverse_type = selected_rel
                print(f"\n¿Está seguro que desea establecer la siguiente relación?")
                print(f"{person1['nombres']} {person1['apellidos']} es {label.lower()} de {person2['nombres']} {person2['apellidos']}")
                
                confirm = input("\n¿Confirmar? (s/n): ").strip().lower()
                if confirm != 's':
                    continue
                    
                # Establecer la relación en ambas direcciones
                success1 = add_relationship(
                    person1['id_persona'], 
                    person2['id_persona'], 
                    rel_type, 
                    user_id
                )
                
                # Establecer la relación inversa
                success2 = add_relationship(
                    person2['id_persona'], 
                    person1['id_persona'], 
                    inverse_type, 
                    user_id
                )
                
                if success1 and success2:
                    show_message("✅ Relación familiar establecida exitosamente.", "success")
                else:
                    show_message("❌ Error al establecer la relación. Intente nuevamente.", "error")
                
                input("\nPresione ENTER para continuar...")
                return
                
            # Si llegamos aquí, el usuario quiere seleccionar otra relación
            if input("\n¿Desea seleccionar otro tipo de relación? (s/n): ").lower() != 's':
                break
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
