from typing import Dict, Any
from ..person import get_person_by_id
from ..relationship import get_relationships

def get_family_tree(person_id: int, max_depth: int = 3, current_depth: int = 0) -> Dict[str, Any]:
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
