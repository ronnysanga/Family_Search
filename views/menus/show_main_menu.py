from utils.console_utils import show_header, get_input, clear_screen

def show_main_menu() -> str:
    clear_screen()
    show_header("Menú Principal")
    print("\n1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    
    while True:
        choice = get_input("\nSeleccione una opción: ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("\n❌ Opción no válida. Intente nuevamente.")
