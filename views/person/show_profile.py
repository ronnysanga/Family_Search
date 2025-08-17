from typing import Optional, Dict, Any
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.person import get_person_by_id
from ..family_tree import show_family_tree

def show_profile(user_id: int, person_id: Optional[int] = None) -> None:
    """
    Display a person's profile with their details and options to edit or view family tree.
    
    Args:
        user_id: ID of the currently logged-in user
        person_id: Optional ID of the person to display (defaults to user's own profile)
    """
    if not person_id:
        person_id = user_id
    
    person = get_person_by_id(person_id)
    if not person:
        show_message("Persona no encontrada.", "error")
        return
    
    while True:
        clear_screen()
        show_header(f"Perfil de {person['nombres']} {person['apellidos']}")
        
        # Display person details
        print("\n" + "="*50)
        print(f"Nombres: {person['nombres']}")
        print(f"Apellidos: {person['apellidos']}")
        
        if 'fecha_nacimiento' in person and person['fecha_nacimiento']:
            print(f"Fecha de Nacimiento: {person['fecha_nacimiento']}")
        
        if 'sexo' in person and person['sexo']:
            sexo = person['sexo'].lower()
            if sexo == 'masculino' or sexo == 'm':
                print("Sexo: Masculino")
            elif sexo == 'femenino' or sexo == 'f':
                print("Sexo: Femenino")
            
        if 'lugar_nacimiento' in person and person['lugar_nacimiento']:
            print(f"Lugar de Nacimiento: {person['lugar_nacimiento']}")
            
        if 'biografia' in person and person['biografia']:
            print("\nBiografía:")
            print("-"*50)
            print(person['biografia'])
            
        print("\n" + "="*50)
        
        # Show menu options
        print("\nOpciones:")
        if str(person_id) == str(user_id):
            print("1. Editar perfil")
        print("2. Ver árbol genealógico")
        print("3. Volver al menú principal")
        
        choice = get_input("\nSeleccione una opción: ").strip()
        
        if choice == '1' and str(person_id) == str(user_id):
            from .show_edit_form import show_edit_form
            show_edit_form(person, user_id)
            # Refresh person data after editing
            person = get_person_by_id(person_id)
        elif choice == '2':
            show_family_tree(person_id)
        elif choice == '3':
            return
        else:
            show_message("Opción no válida. Intente nuevamente.", "error")
            input("Presione ENTER para continuar...")
