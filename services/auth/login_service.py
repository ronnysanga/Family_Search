from typing import Optional, Dict, Any
from database import create_connection, close_connection
from utils.password_utils import verify_password

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    if not email or not password:
        return None
        
    connection = None
    cursor = None
    
    try:
        connection = create_connection()
        if not connection:
            return None
            
        # Configurar el cursor para leer todos los resultados
        cursor = connection.cursor(dictionary=True, buffered=True)
        
        query = """
        SELECT u.id_usuario, u.email, u.password, u.nombres, u.apellidos,
               p.id_persona
        FROM usuario u
        LEFT JOIN persona p ON u.id_usuario = p.id_usuario_creador
        WHERE u.email = %s
        LIMIT 1
        """
        cursor.execute(query, (email,))
        
        # Asegurarse de leer todos los resultados
        user = cursor.fetchone()
        
        # Consumir cualquier resultado pendiente
        if cursor.with_rows:
            cursor.fetchall()
        
        if not user:
            return None
            
        # Verificar contraseña
        if not verify_password(user.get('password', ''), password):
            return None
            
        # Eliminar la contraseña antes de devolver
        if 'password' in user:
            del user['password']
            
        return user
        
    except Exception as e:
        print(f"Error durante la autenticación: {e}")
        return None
        
    finally:
        # Cerrar cursor y conexión de manera segura
        try:
            if cursor:
                cursor.close()
        except Exception as e:
            print(f"Error al cerrar el cursor: {e}")
            
        try:
            if connection and connection.is_connected():
                close_connection(connection)
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
