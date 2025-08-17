from services.person import search_people
from utils.console_utils import show_header, show_message, clear_screen

def show_search_people():
    """Display the people search interface."""
    show_header("Buscar Personas")
    search_term = input("Ingrese nombre o apellido (deje en blanco para ver todos): ").strip()
    
    results = search_people(search_term)
    
    show_header(f"Resultados de Búsqueda ({len(results)})")
    
    if not results:
        show_message("No se encontraron personas que coincidan con la búsqueda.")
    else:
        for i, person in enumerate(results, 1):
            birth_info = f"Nacido en {person['lugar_nacimiento']} " if person['lugar_nacimiento'] else ""
            birth_date = f"el {person['fecha_nacimiento'].strftime('%d/%m/%Y')} " if person['fecha_nacimiento'] else ""
            print(f"{i}. {person['apellidos']}, {person['nombres']} - {birth_date}{birth_info}")
    
    input("\nPresione Enter para continuar...")

def search_and_select_person(prompt="Buscar persona"):
    """
    Permite buscar y seleccionar una persona de la base de datos.
    
    Returns:
        dict or None: Información de la persona seleccionada o None si se cancela
    """
    while True:
        clear_screen()
        show_header(prompt)
        search_term = input("Ingrese nombre o apellido (o deje en blanco para ver todos, 'salir' para cancelar): ").strip()
        
        if search_term.lower() == 'salir':
            return None
            
        results = search_people(search_term)
        
        if not results:
            show_message("No se encontraron personas que coincidan con la búsqueda.", "warning")
            input("Presione Enter para continuar...")
            continue
            
        # Mostrar resultados
        clear_screen()
        show_header(f"Resultados de búsqueda ({len(results)})")
        for i, person in enumerate(results, 1):
            birth_info = f" | Nacimiento: {person['fecha_nacimiento'].strftime('%d/%m/%Y')}" if person.get('fecha_nacimiento') else ""
            print(f"{i}. {person['apellidos']}, {person['nombres']}{birth_info}")
            
        # Permitir al usuario seleccionar una persona
        while True:
            try:
                selection = input("\nSeleccione un número (o 0 para buscar de nuevo): ").strip()
                if not selection:
                    continue
                    
                choice = int(selection)
                if choice == 0:
                    break
                elif 1 <= choice <= len(results):
                    return results[choice - 1]
                else:
                    show_message("Número fuera de rango. Intente nuevamente.", "error")
            except ValueError:
                show_message("Por favor ingrese un número válido.", "error")
