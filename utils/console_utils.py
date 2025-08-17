import os

def print_colored(text, color=None, style=None, end='\n'):
    """
    Imprime texto con colores en la consola.
    
    Args:
        text (str): Texto a imprimir
        color (str, optional): Color del texto. Opciones: 'black', 'red', 'green', 'yellow', 
                             'blue', 'magenta', 'cyan', 'white'.
        style (str, optional): Estilo del texto. Opciones: 'bold', 'underline', 'reverse'.
        end (str, optional): Carácter de fin de línea. Por defecto es '\n'.
    """
    colors = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
        'reset': '0'
    }
    
    styles = {
        'bold': '1',
        'underline': '4',
        'reverse': '7',
        'reset': '0'
    }
    
    color_code = ''
    style_code = ''
    
    if color and color in colors:
        color_code = f'\033[{colors[color]}m'
    
    if style and style in styles:
        style_code = f'\033[{styles[style]}m'
    
    reset_code = '\033[0m' if color_code or style_code else ''
    
    print(f"{color_code}{style_code}{text}{reset_code}", end=end)


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
