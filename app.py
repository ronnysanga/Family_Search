import os
import sys
from dotenv import load_dotenv
from views.auth.login_view import show_login_form
from views.auth.show_register_form import show_register_form
from views.menus.show_main_menu import show_main_menu
from views.menus.show_logged_in_menu import show_logged_in_menu
from views.person import show_profile, show_add_form, show_edit_form, show_search, select_person
from views.family_tree import show_family_tree, show_add_relationship

def handle_logged_in_choice(choice: str, user_id: int) -> str:
    """Handle user's choice from the logged-in menu."""
    if choice == '1':  # View profile
        show_profile(user_id)
    elif choice == '2':  # Search people
        show_search()
    elif choice == '3':  # Add person
        show_add_form(user_id)
    elif choice == '4':  # Edit person
        person = select_person("Seleccione la persona a editar")
        if person:
            show_edit_form(person, user_id)
    elif choice == '5':  # View family tree
        show_family_tree()
    elif choice == '6':  # Add relationship
        show_add_relationship(user_id)
    elif choice == '7':  # Logout
        return 'logout'
        
    return ''

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
            choice = show_logged_in_menu(current_user['id_usuario'])
            
            # Handle user's choice
            if choice == 'logout':
                current_user = None
            else:
                result = handle_logged_in_choice(choice, current_user['id_usuario'])
                if result == 'logout':
                    current_user = None

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
        sys.exit(0)
