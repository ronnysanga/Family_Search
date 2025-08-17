import sys
from utils.console_utils import show_header, get_input

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
        print("4. Cerrar sesión")
        
        choice = get_input("\nSeleccione una opción: ")
        
        if choice in ['1', '2', '3', '4']:
            return choice
        
        print("\nOpción no válida. Intente nuevamente.")
        input("Presione Enter para continuar...")
