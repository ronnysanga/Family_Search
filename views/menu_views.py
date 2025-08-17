from utils.console_utils import show_header, get_input, clear_screen, show_message
from .person import show_edit_person_form, show_profile, show_search_people, show_add_person_form
from .family_tree import show_family_tree_menu

def show_main_menu():
    """Display the main menu and handle user input."""
    while True:
        show_header("Menú Principal")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        
        choice = get_input("\nSeleccione una opción: ")
        
        if choice in ['1', '2', '3']:
            return choice
        
        print("\nOpción no válida. Intente nuevamente.")
        input("Presione Enter para continuar...")

def show_logged_in_menu(user_id):
    """Display the menu for logged-in users."""
    while True:
        show_header("Menú Principal")
        print("1. Ver perfil")
        print("2. Buscar personas")
        print("3. Agregar persona")
        print("4. Editar persona")
        print("5. Árbol genealógico")
        print("6. Cerrar sesión")
        
        choice = get_input("\nSeleccione una opción: ")
        
        if choice == '1':
            show_profile(user_id)
            input("\nPresione Enter para continuar...")
        elif choice == '2':
            show_search_people()
        elif choice == '3':
            show_add_person_form(user_id)
            input("\nPresione Enter para continuar...")
        elif choice == '4':
            show_edit_person_form(user_id)
        elif choice == '5':
            show_family_tree_menu(user_id)
        elif choice == '6':
            if input("\n¿Está seguro que desea cerrar sesión? (s/n): ").lower() == 's':
                show_message("Sesión cerrada exitosamente.", "success")
                return 'logout'
        else:
            show_message("Opción no válida. Intente nuevamente.", "error")
            input("Presione Enter para continuar...")
