import os
from typing import Tuple

def load_environment() -> bool:
    """Load environment variables from .env file."""
    from dotenv import load_dotenv
    return load_dotenv()

def check_environment() -> Tuple[bool, str]:
    """Check if required environment variables are set."""
    if not os.path.exists('.env'):
        return False, "Error: No se encontró el archivo .env"
    
    # Load environment variables
    load_environment()
    
    # Check required environment variables
    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        error_msg = (
            f"Error: Faltan variables de entorno requeridas: {', '.join(missing_vrs)}. "
            "Por favor, asegúrese de que el archivo .env contenga todas las variables necesarias."
        )
        return False, error_msg
    
    return True, ""
