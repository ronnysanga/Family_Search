import os
import sys
from dotenv import load_dotenv
from views.auth.login_view import show_login_form
from views.auth.show_register_form import show_register_form
from views.menus.show_main_menu import show_main_menu
from views.menus.show_logged_in_menu import show_logged_in_menu
from views.person import show_profile, show_add_form, show_edit_form, show_search, select_person

def handle_logged_in_choice(choice: str, user_id: int) -> str:
    if choice == '1':  
        show_profile(user_id)
    elif choice == '2':  
        show_search()
    elif choice == '3': 
        show_add_form(user_id)
    elif choice == '4': 
        person = select_person("Seleccione la persona a editar")
        if person:
            show_edit_form(person, user_id)
    elif choice == '5':  
        from views.family_tree.show_add_relationship import show_add_relationship
        show_add_relationship(user_id)
    elif choice == '6':  
        from views.family_tree.show_tree import show_family_tree
        show_family_tree(user_id)
    elif choice == '7':  
        return 'logout'
        
    return ''

def main():
    """Main function to start the application."""
    if not os.path.exists('.env'):
        print("Error: No se encontró el archivo .env")
        print("Por favor, cree un archivo .env basado en .env.example")
        return
    
    load_dotenv()
    
    current_user = None
    
    while True:
        if current_user is None:
            choice = show_main_menu()
            
            if choice == '1':  
                user = show_login_form()
                if user:
                    current_user = user
                
            elif choice == '2': 
                show_register_form()
                input("\nPresione Enter para continuar...")
                
            elif choice == '3':  
                print("\n¡Hasta luego!")
                sys.exit(0)
                
        else:
            choice = show_logged_in_menu(current_user['id_usuario'])

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
