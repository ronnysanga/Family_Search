from typing import Optional, Dict, Any
from database import create_connection, close_connection
from utils.password_utils import verify_password

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with email and password.
    
    Args:
        email: User's email
        password: Plain text password
        
    Returns:
        User data if authentication succeeds, None otherwise
    """
    if not email or not password:
        return None
        
    connection = create_connection()
    if not connection:
        return None
        
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT u.id_usuario, u.email, u.password, u.nombres, u.apellidos,
               p.id_persona
        FROM usuario u
        LEFT JOIN persona p ON u.id_usuario = p.id_usuario_creador
        WHERE u.email = %s
        """
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
        if not user:
            return None
            
        # Verify password
        if not verify_password(user['password'], password):
            return None
            
        # Remove password before returning
        user.pop('password', None)
        return user
        
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None
        
    finally:
        cursor.close()
        close_connection(connection)
