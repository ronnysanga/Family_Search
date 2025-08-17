from typing import Callable, Dict, Any
from utils.console_utils import show_header, get_input, clear_screen, show_message

def show_logged_in_menu(user_id: int) -> str:
    menu_options = {
        '1': 'Ver perfil',
        '2': 'Buscar personas',
        '3': 'Agregar persona',
        '4': 'Editar persona',
        '5': 'Cerrar sesión'
    }
    
    while True:
        clear_screen()
        show_header("Menú Principal")
        
        # Display menu options
        for key, option in menu_options.items():
            print(f"{key}. {option}")
            
        choice = get_input("\nSeleccione una opción: ").strip()
        
        if choice == '5':  # Logout
            confirm = input("\n¿Está seguro que desea cerrar sesión? (s/n): ").strip().lower()
            if confirm == 's':
                show_message("Sesión cerrada exitosamente.", "success")
                return 'logout'
        elif choice in menu_options:
            return choice
        else:
            show_message("Opción no válida. Intente nuevamente.", "error")
            input("Presione ENTER para continuar...")
