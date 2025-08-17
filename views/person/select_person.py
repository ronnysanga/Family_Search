from typing import Optional, Dict, Any
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.person.search import search_people

def select_person(prompt: str = "Buscar persona") -> Optional[Dict[str, Any]]:
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
            
        # Perform search
        results = search_people(search_term) if search_term else search_people("")
        
        if not results:
            print("\n" + "-"*50)
            print("No se encontraron personas que coincidan con la búsqueda.")
            input("\nPresione ENTER para intentar de nuevo...")
            continue
            
        # Display search results
        while True:
            clear_screen()
            show_header("Resultados de Búsqueda")
            print(f"Se encontraron {len(results)} personas:")
            print("-"*80)
            
            # Display results in a table
            print(f"{'#':<4} {'NOMBRES':<25} {'APELLIDOS':<25} {'NACIMIENTO':<12} {'SEXO':<6}")
            print("-"*80)
            
            for i, person in enumerate(results, 1):
                nombres = person.get('nombres', '')[:20]
                apellidos = person.get('apellidos', '')[:20]
                fecha_nac = str(person.get('fecha_nacimiento', ''))[:10]
                sexo = person.get('sexo', '').lower()
                sexo_display = ''
                if sexo == 'masculino' or sexo == 'm':
                    sexo_display = 'M'
                elif sexo == 'femenino' or sexo == 'f':
                    sexo_display = 'F'
                
                print(f"{i:<4} {nombres:<25} {apellidos:<25} {fecha_nac:<12} {sexo_display:<6}")
            
            # Show options
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
            
            # Invalid option
            show_message("Opción no válida. Intente nuevamente.", "error")
            input("Presione ENTER para continuar...")
