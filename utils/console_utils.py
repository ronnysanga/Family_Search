import os

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header(title):
    """Display a formatted header."""
    clear_screen()
    print(f"=== {title.upper()} ===\n")

def show_message(message, message_type="info"):
    """Display a formatted message."""
    if message_type == "error":
        print(f"\n[!] {message}")
    elif message_type == "success":
        print(f"\n[✓] {message}")
    else:
        print(f"\n[i] {message}")

def get_input(prompt, required=True, input_type=str, password=False):
    """
    Get user input with validation.
    
    Args:
        prompt (str): The prompt to display to the user
        required (bool): Whether the input is required
        input_type (type): The expected data type of the input
        password (bool): If True, input will be hidden (for passwords)
        
    Returns:
        The user input converted to the specified type, or None if input is empty and not required
    """
    while True:
        try:
            if password:
                import getpass
                value = getpass.getpass(prompt)
            else:
                value = input(prompt).strip()
                
            if not value:
                if required:
                    show_message("Este campo es requerido.", "error")
                    continue
                return None
                
            # Si el tipo es str, devolver el valor tal cual
            if input_type == str:
                return value
                
            # Para otros tipos, intentar la conversión
            return input_type(value)
            
        except ValueError:
            show_message(f"Por favor ingrese un valor válido de tipo {input_type.__name__}.", "error")

def show_menu(options, prompt="Seleccione una opción: "):
    """
    Muestra un menú interactivo y devuelve el índice de la opción seleccionada.
    
    Args:
        options: Lista de tuplas (texto_opcion, funcion)
        prompt: Mensaje a mostrar para la selección
        
    Returns:
        int: Índice de la opción seleccionada (0-based) o None si se cancela
    """
    while True:
        show_header("Menú de Opciones")
        
        # Mostrar opciones
        for i, (text, _) in enumerate(options, 1):
            print(f"{i}. {text}")
            
        # Obtener selección del usuario
        try:
            choice = input(f"\n{prompt}").strip()
            if not choice:
                return None
                
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
                
            show_message(f"Por favor ingrese un número entre 1 y {len(options)}.", "error")
        except ValueError:
            show_message("Por favor ingrese un número válido.", "error")
