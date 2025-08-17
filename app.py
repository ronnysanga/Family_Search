import os
import sys
from dotenv import load_dotenv

# Import views
from views.auth_views import show_register_form, show_login_form
from views.person_views import show_profile, show_search_people, show_add_person_form
from views.menu_views import show_main_menu, show_logged_in_menu
from views.family_tree_views import show_family_tree_menu

def main():
    """Main function to start the application."""
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Error: No se encontró el archivo .env")
        print("Por favor, cree un archivo .env basado en .env.example")
        return
    
    # Load environment variables
    load_dotenv()
    
    # Main application loop
    current_user = None
    
    while True:
        if current_user is None:
            # Show main menu for non-authenticated users
            choice = show_main_menu()
            
            if choice == '1':  # Login
                user = show_login_form()
                if user:
                    current_user = user
                
            elif choice == '2':  # Register
                show_register_form()
                input("\nPresione Enter para continuar...")
                
            elif choice == '3':  # Exit
                print("\n¡Hasta luego!")
                sys.exit(0)
                
        else:
            # Show menu for authenticated users
            result = show_logged_in_menu(current_user['id_usuario'])
            
            # Si el resultado es 'logout', cerramos la sesión
            if result == 'logout':
                current_user = None
                input("Presione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
        sys.exit(0)
