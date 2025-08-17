"""
Family Tree Service Module

This module provides functional programming style functions for managing family trees.
It allows users to create and visualize their family trees with relationships.
"""
from typing import Dict, List, Optional, Tuple, Callable, Any
from functools import reduce
import operator
from database import create_connection, close_connection
from utils.console_utils import show_message, get_input, show_header

# Type aliases
Person = Dict[str, Any]
Relationship = Dict[str, Any]

# Database connection helper
def with_db_connection(func: Callable) -> Callable:
    """Decorator to handle database connections"""
    def wrapper(*args, **kwargs):
        conn = create_connection()
        if not conn:
            show_message("Error al conectar a la base de datos.", "error")
            return None
        try:
            return func(conn, *args, **kwargs)
        except Exception as e:
            show_message(f"Error inesperado: {e}", "error")
            return None
        finally:
            close_connection(conn)
    return wrapper

# Person operations
get_person_by_id = with_db_connection(
    lambda conn, person_id: 
        conn.cursor(dictionary=True).execute(
            """
            SELECT p.*, 
                   DATE_FORMAT(p.fecha_nacimiento, '%d/%m/%Y') as fecha_nac_formateada,
                   DATE_FORMAT(p.fecha_defuncion, '%d/%m/%Y') as fecha_def_formateada
            FROM persona p 
            WHERE p.id_persona = %s
            """,
            (person_id,)
        ).fetchone()
)

search_people = with_db_connection(
    lambda conn, search_term, limit=50: 
        conn.cursor(dictionary=True).execute(
            """
            SELECT id_persona, nombres, apellidos, 
                   DATE_FORMAT(fecha_nacimiento, '%d/%m/%Y') as fecha_nac,
                   sexo
            FROM persona 
            WHERE nombres LIKE %s OR apellidos LIKE %s
            ORDER BY apellidos, nombres
            LIMIT %s
            """,
            (f"%{search_term}%", f"%{search_term}%", limit)
        ).fetchall()
)

def create_person(person_data: Dict, user_id: int) -> Optional[int]:
    """Create a new person in the database"""
    @with_db_connection
    def _create_person(conn, person_data, user_id):
        cursor = conn.cursor()
        query = """
        INSERT INTO persona (
            id_usuario_creador, nombres, apellidos, fecha_nacimiento,
            fecha_defuncion, sexo, lugar_nacimiento, lugar_defuncion, biografia
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_id,
            person_data['nombres'],
            person_data['apellidos'],
            person_data.get('fecha_nacimiento'),
            person_data.get('fecha_defuncion'),
            person_data.get('sexo', 'masculino'),
            person_data.get('lugar_nacimiento'),
            person_data.get('lugar_defuncion'),
            person_data.get('biografia')
        ))
        conn.commit()
        return cursor.lastrowid
    
    return _create_person(person_data, user_id)

# Relationship operations
get_relationships = with_db_connection(
    lambda conn, person_id: 
        conn.cursor(dictionary=True).execute(
            """
            SELECT 
                rf.id_relacion,
                p2.id_persona as id_pariente,
                CONCAT(p2.nombres, ' ', p2.apellidos) as nombre_pariente,
                rf.tipo_relacion
            FROM relacion_familiar rf
            JOIN persona p1 ON rf.id_persona1 = p1.id_persona
            JOIN persona p2 ON rf.id_persona2 = p2.id_persona
            WHERE rf.id_persona1 = %s
            """,
            (person_id,)
        ).fetchall()
)

def add_relationship(person1_id: int, person2_id: int, relationship_type: str, user_id: int) -> bool:
    """Add a family relationship between two people"""
    @with_db_connection
    def _add_relationship(conn, person1_id, person2_id, relationship_type, user_id):
        if person1_id == person2_id:
            show_message("No se puede establecer una relación consigo mismo.", "error")
            return False
            
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO relacion_familiar 
                (id_persona1, id_persona2, tipo_relacion, id_usuario_creador)
                VALUES (%s, %s, %s, %s)
                """,
                (person1_id, person2_id, relationship_type, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            if "Duplicate entry" in str(e):
                show_message("Esta relación ya existe.", "warning")
            else:
                show_message(f"Error al establecer la relación: {e}", "error")
            return False
    
    return _add_relationship(person1_id, person2_id, relationship_type, user_id)

# Family tree visualization
def get_family_tree(person_id: int, max_depth: int = 3, current_depth: int = 0) -> Dict:
    """
    Recursively build a family tree structure
    
    Args:
        person_id: ID of the root person
        max_depth: Maximum depth to traverse
        current_depth: Current depth in the recursion
        
    Returns:
        A dictionary representing the person and their relationships
    """
    if current_depth >= max_depth:
        return {}
        
    person = get_person_by_id(person_id)
    if not person:
        return {}
        
    relationships = get_relationships(person_id)
    
    # Process relationships and build tree
    tree = {
        'id': person['id_persona'],
        'name': f"{person['nombres']} {person['apellidos']}",
        'birth_date': person['fecha_nac_formateada'],
        'relationships': {}
    }
    
    for rel in relationships:
        rel_type = rel['tipo_relacion']
        if rel_type not in tree['relationships']:
            tree['relationships'][rel_type] = []
            
        # Get the person's details and their relationships
        person_data = {
            'id': rel['id_pariente'],
            'name': rel['nombre_pariente'],
            'relationship': rel_type
        }
        
        # Recursively get family members if we haven't reached max depth
        if current_depth < max_depth - 1:
            person_data['family'] = get_family_tree(
                rel['id_pariente'], 
                max_depth, 
                current_depth + 1
            )
            
        tree['relationships'][rel_type].append(person_data)
    
    return tree

def print_family_tree(person_id: int, max_depth: int = 3):
    """Print a text-based representation of the family tree"""
    def _print_node(node, level=0, prefix=''):
        if not node:
            return
            
        # Print person's name
        indent = '    ' * level
        print(f"{indent}{prefix}{node['name']}")
        
        # Print relationships if any
        if 'relationships' in node:
            for rel_type, people in node['relationships'].items():
                print(f"{indent}  ├─ {rel_type.upper()}:")
                for i, person in enumerate(people, 1):
                    is_last = i == len(people)
                    new_prefix = '└─ ' if is_last else '├─ '
                    _print_node(person, level + 1, new_prefix)
    
    # Start building the tree from the root person
    tree = get_family_tree(person_id, max_depth)
    if tree:
        _print_node(tree)
    else:
        show_message("No se pudo generar el árbol genealógico.", "error")
