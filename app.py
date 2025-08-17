import os
import sys
from dotenv import load_dotenv

# Import views
from views.auth_views import show_register_form, show_login_form
from views.person_views import show_profile, show_search_people, show_add_person_form
from views.menu_views import show_main_menu, show_logged_in_menu

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
            
            if choice == '1':  # View profile
                show_profile(current_user['id_usuario'])
                
            elif choice == '2':  # Search people
                show_search_people()
                
            elif choice == '3':  # Add person
                show_add_person_form(current_user['id_usuario'])
                
            elif choice == '4':  # Logout
                current_user = None
                print("\nSesión cerrada exitosamente.")
                input("Presione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
        sys.exit(0)
