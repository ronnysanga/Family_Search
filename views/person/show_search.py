from typing import List, Dict, Any, Optional
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.person.search import search_people
from ..family_tree import show_family_tree

def show_search() -> None:
    while True:
        clear_screen()
        show_header("Búsqueda de Personas")
        
        print("\nIngrese el nombre, apellido o parte de estos.")
        print("Presione ENTER sin escribir para ver todas las personas.")
        print("Escriba 'salir' para volver al menú principal.")
        
        search_term = input("\n🔍 Búsqueda: ").strip()
        
        if search_term.lower() == 'salir':
            return
            
        # Perform search
        results = search_people(search_term) if search_term else search_people("")
        
        if not results:
            print("\n" + "-"*50)
            print("No se encontraron personas que coincidan con la búsqueda.")
            input("\nPresione ENTER para intentar de nuevo...")
            continue
            
        # Display search results with pagination
        page = 0
        per_page = 10
        total_pages = (len(results) + per_page - 1) // per_page
        
        while True:
            clear_screen()
            show_header("Resultados de Búsqueda")
            print(f"Mostrando {len(results)} resultados (página {page + 1} de {max(1, total_pages)}):")
            print("-"*80)
            
            # Display current page of results
            start_idx = page * per_page
            end_idx = min(start_idx + per_page, len(results))
            
            print(f"{'#':<4} {'NOMBRES':<25} {'APELLIDOS':<25} {'NACIMIENTO':<12} {'SEXO':<6}")
            print("-"*80)
            
            for i in range(start_idx, end_idx):
                person = results[i]
                nombres = person.get('nombres', '')[:20]
                apellidos = person.get('apellidos', '')[:20]
                fecha_nac = str(person.get('fecha_nacimiento', ''))[:10]
                sexo = person.get('sexo', '')[:1].upper()
                
                print(f"{i+1:<4} {nombres:<25} {apellidos:<25} {fecha_nac:<12} {sexo:<6}")
            
            # Show navigation options
            print("\n" + "-"*80)
            print("INSTRUCCIONES:")
            print(f"- Ingrese un número del 1 al {end_idx-start_idx} para seleccionar una persona")
            
            if total_pages > 1:
                if page > 0:
                    print("- 'a' para página anterior")
                if page < total_pages - 1:
                    print("- 's' para página siguiente")
            
            print("- 'b' para buscar de nuevo")
            print("- 'm' para volver al menú principal")
            
            choice = input("\nSu elección: ").strip().lower()
            
            # Handle navigation
            if choice == 'm':
                return
            elif choice == 'b':
                break
            elif choice == 'a' and page > 0:
                page -= 1
            elif choice == 's' and page < total_pages - 1:
                page += 1
            elif choice.isdigit():
                idx = int(choice) - 1 + start_idx
                if 0 <= idx < len(results):
                    _handle_person_selection(results[idx])
            else:
                show_message("Opción no válida. Intente nuevamente.", "error")
                input("Presione ENTER para continuar...")

def _handle_person_selection(person: Dict[str, Any]) -> None:
    """
    Handle actions after selecting a person from search results.
    
    Args:
        person: Dictionary containing the selected person's data
    """
    while True:
        clear_screen()
        show_header(f"Opciones para {person['nombres']} {person['apellidos']}")
        
        print("\nSeleccione una opción:")
        print("1. Ver perfil")
        print("2. Ver árbol genealógico")
        print("3. Volver a resultados")
        
        choice = input("\nOpción: ").strip()
        
        if choice == '1':
            from .show_profile import show_profile
            show_profile(person['id_persona'])
        elif choice == '2':
            show_family_tree(person['id_persona'])
        elif choice == '3':
            return
        else:
            show_message("Opción no válida. Intente nuevamente.", "error")
            input("Presione ENTER para continuar...")
