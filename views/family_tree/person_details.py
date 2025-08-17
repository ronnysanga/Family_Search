from typing import Dict, Any
from services.person import get_person_by_id
from utils.console_utils import show_header, show_message, clear_screen

def show_person_details(person_id: str):
    """Show detailed information about a person"""
    try:
        person = get_person_by_id(int(person_id))
        if not person:
            show_message("No se encontró a la persona.", "error")
            return
            
        clear_screen()
        show_header(f"Detalles de {person['nombres']} {person['apellidos']}")
        
        # Mostrar información básica
        print("\nInformación Personal:")
        print(f"  • Nombres: {person.get('nombres', 'No especificado')}")
        print(f"  • Apellidos: {person.get('apellidos', 'No especificado')}")
        
        if 'fecha_nac_formateada' in person:
            print(f"  • Fecha de nacimiento: {person['fecha_nac_formateada']}")
        
        if 'fecha_def_formateada' in person:
            print(f"  • Fecha de defunción: {person['fecha_def_formateada']}")
            
        if 'sexo' in person and person['sexo']:
            sexo = person['sexo'].lower()
            if sexo == 'masculino' or sexo == 'm':
                print("  • Sexo: Masculino")
            elif sexo == 'femenino' or sexo == 'f':
                print("  • Sexo: Femenino")
            else:
                print("  • Sexo: No especificado")
            
        if 'lugar_nacimiento' in person and person['lugar_nacimiento']:
            print(f"  • Lugar de nacimiento: {person['lugar_nacimiento']}")
            
        if 'biografia' in person and person['biografia']:
            print("\nBiografía:")
            print(person['biografia'])
        
        input("\nPresione Enter para continuar...")
        
    except ValueError:
        show_message("ID de persona no válido.", "error")
