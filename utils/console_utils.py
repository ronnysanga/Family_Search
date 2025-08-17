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

def get_input(prompt, required=True, input_type=str):
    """Get user input with validation."""
    while True:
        try:
            value = input(prompt).strip()
            if required and not value:
                show_message("Este campo es requerido.", "error")
                continue
            return input_type(value)
        except ValueError:
            show_message(f"Por favor ingrese un valor válido de tipo {input_type.__name__}.", "error")
