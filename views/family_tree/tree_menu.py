from utils.console_utils import show_header, get_input, clear_screen, show_message
from .tree_view import show_family_tree_view
from .relationship_views import show_add_relationship

def show_family_tree_menu(user_id: int):
    """Show the main family tree management menu"""
    while True:
        clear_screen()
        show_header("Menú de Árbol Genealógico")
        
        print("1. Ver árbol genealógico")
        print("2. Agregar relación familiar")
        print("3. Volver al menú principal")
        
        option = get_input("\nSeleccione una opción: ")
        
        if option == '1':
            show_family_tree_view()
        elif option == '2':
            show_add_relationship(user_id)
        elif option == '3':
            return
        else:
            show_message("Opción no válida. Intente nuevamente.", "error")
