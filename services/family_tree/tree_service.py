from typing import Dict

from ..person import get_person_by_id
from .relationship_service import get_relationships
from utils.console_utils import show_message

def get_family_tree(person_id: int, max_depth: int = 3, current_depth: int = 0) -> Dict:
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
        'birth_date': person.get('fecha_nac_formateada', ''),
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
