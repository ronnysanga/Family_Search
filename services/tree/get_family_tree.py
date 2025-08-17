from typing import Dict, Any, List, Optional, Set, Tuple
from ..person import get_person_by_id
from ..relationship import get_relationships

def _build_relationships_cache(person_id: int, max_depth: int, current_depth: int) -> Tuple[Dict[int, Dict], Set[int]]:
    """
    Construye un caché de relaciones para evitar múltiples consultas a la base de datos.
    
    Args:
        person_id: ID de la persona actual
        max_depth: Profundidad máxima del árbol
        current_depth: Profundidad actual
        
    Returns:
        Tupla con (personas_por_id, visitados)
    """
    if current_depth > max_depth:
        return {}, set()
        
    # Obtener información de la persona si no está en caché
    person = get_person_by_id(person_id)
    if not person:
        return {}, set()
        
    personas_por_id = {person_id: person}
    visitados = {person_id}
    relaciones_por_persona = {person_id: get_relationships(person_id)}
    
    # Si hemos alcanzado la profundidad máxima, no explorar más
    if current_depth == max_depth:
        return personas_por_id, visitados
    
    # Obtener relaciones y explorar recursivamente
    for rel in relaciones_por_persona[person_id]:
        relative_id = rel['id_pariente']
        if relative_id not in visitados:
            # Obtener subárbol del familiar
            sub_arbol, sub_visitados = _build_relationships_cache(
                relative_id, max_depth, current_depth + 1
            )
            # Actualizar cachés
            personas_por_id.update(sub_arbol)
            visitados.update(sub_visitados)
    
    return personas_por_id, visitados

def build_family_tree(person_id: int, max_depth: int = 3, current_depth: int = 0, 
                     visited: Optional[Set[int]] = None, 
                     cache: Optional[Dict[int, Dict]] = None) -> Dict[str, Any]:
    """
    Construye un árbol genealógico como un diccionario anidado.
    
    Args:
        person_id: ID de la persona raíz del árbol
        max_depth: Profundidad máxima del árbol
        current_depth: Profundidad actual (para recursión)
        visited: Conjunto de IDs de personas ya visitadas (para evitar ciclos)
        cache: Diccionario con información en caché de las personas
        
    Returns:
        Un diccionario que representa el árbol genealógico de la persona
    """
    if visited is None:
        visited = set()
        
    # Evitar ciclos infinitos
    if person_id in visited:
        return {}
        
    visited.add(person_id)
    
    # Obtener información de la persona desde la caché o la base de datos
    if cache is not None and person_id in cache:
        person = cache[person_id]
    else:
        person = get_person_by_id(person_id)
        
    if not person:
        return {}
    
    # Crear nodo de la persona actual
    person_node = _create_person_node(person)
    
    # Si hemos alcanzado la profundidad máxima, retornar solo los datos de la persona
    if current_depth >= max_depth:
        return person_node
    
    # Obtener todas las relaciones de la persona
    relationships = get_relationships(person_id)
    
    # Procesar cada relación
    for rel in relationships:
        relative_id = rel['id_pariente']
        rel_type = rel['tipo_relacion']
        
        # Evitar ciclos infinitos
        if relative_id in visited:
            continue
            
        # Obtener información del familiar desde la caché o la base de datos
        if cache is not None and relative_id in cache:
            relative = cache[relative_id]
        else:
            relative = get_person_by_id(relative_id)
            
        if not relative:
            continue
            
        # Crear nodo del familiar
        relative_data = _create_relative_node(relative, rel_type)
        
        # Clasificar la relación
        _classify_relationship(person_node, relative_data, rel_type)
            
        # Recursión para construir el árbol de los familiares
        if rel_type in ['padre', 'madre', 'hijo', 'hija'] and current_depth < max_depth - 1:
            relative_tree = build_family_tree(
                relative_id, 
                max_depth, 
                current_depth + 1, 
                visited.copy(),
                cache
            )
            relative_data.update(relative_tree)
    
    return person_node

def _create_person_node(person: Dict[str, Any]) -> Dict[str, Any]:
    """Crea un nodo de persona con la estructura adecuada."""
    return {
        'id': person['id_persona'],
        'nombres': person['nombres'],
        'apellidos': person['apellidos'],
        'sexo': person.get('sexo', ''),
        'fecha_nacimiento': person.get('fecha_nac_formateada', ''),
        'fecha_defuncion': person.get('fecha_def_formateada', ''),
        'lugar_nacimiento': person.get('lugar_nacimiento', ''),
        'lugar_defuncion': person.get('lugar_defuncion', ''),
        'biografia': person.get('biografia', ''),
        'padre': None,
        'madre': None,
        'hijos': [],
        'hermanos': [],
        'esposos': [],
        'otros': []
    }

def _create_relative_node(relative: Dict[str, Any], rel_type: str) -> Dict[str, Any]:
    """Crea un nodo para un familiar con la información relevante."""
    return {
        'id': relative['id_persona'],
        'nombres': relative['nombres'],
        'apellidos': relative['apellidos'],
        'sexo': relative.get('sexo', ''),
        'fecha_nacimiento': relative.get('fecha_nac_formateada', ''),
        'tipo_relacion': rel_type
    }

def _classify_relationship(person_node: Dict[str, Any], 
                          relative_data: Dict[str, Any], 
                          rel_type: str) -> None:
    """Clasifica la relación y la agrega al nodo de la persona."""
    if rel_type == 'padre':
        person_node['padre'] = relative_data
    elif rel_type == 'madre':
        person_node['madre'] = relative_data
    elif rel_type in ['hijo', 'hija']:
        person_node['hijos'].append(relative_data)
    elif rel_type in ['hermano', 'hermana']:
        person_node['hermanos'].append(relative_data)
    elif rel_type in ['esposo', 'esposa']:
        person_node['esposos'].append(relative_data)
    else:
        person_node['otros'].append(relative_data)

def get_family_tree(person_id: int, max_depth: int = 3) -> Dict[str, Any]:
    """
    Obtiene el árbol genealógico de una persona.
    
    Args:
        person_id: ID de la persona
        max_depth: Profundidad máxima del árbol (por defecto: 3)
        
    Returns:
        Un diccionario que representa el árbol genealógico
    """
    # Primero construimos un caché de todas las personas y relaciones
    personas_por_id, _ = _build_relationships_cache(person_id, max_depth, 0)
    
    # Luego construimos el árbol usando el caché
    return build_family_tree(person_id, max_depth, cache=personas_por_id)

def get_ancestors(person_id: int, max_generations: int = 3) -> Dict[str, Any]:
    """
    Obtiene los ancestros de una persona (padres, abuelos, etc.).
    
    Args:
        person_id: ID de la persona
        max_generations: Número máximo de generaciones a incluir
        
    Returns:
        Un diccionario con los ancestros de la persona
    """
    # Construir caché solo para ancestros
    personas_por_id, _ = _build_relationships_cache(person_id, max_generations, 0)
    return build_family_tree(person_id, max_generations, cache=personas_por_id)

def get_descendants(person_id: int, max_generations: int = 3) -> Dict[str, Any]:
    """
    Obtiene los descendientes de una persona (hijos, nietos, etc.).
    
    Args:
        person_id: ID de la persona
        max_generations: Número máximo de generaciones a incluir
        
    Returns:
        Un diccionario con los descendientes de la persona
    """
    # Construir caché solo para descendientes
    def _build_descendants_cache(pid: int, depth: int, current_depth: int, 
                                cache: Dict[int, Dict], visited: Set[int]) -> None:
        if current_depth > depth or pid in visited:
            return
            
        visited.add(pid)
        
        # Obtener información de la persona si no está en caché
        if pid not in cache:
            person = get_person_by_id(pid)
            if person:
                cache[pid] = person
            else:
                return
        
        # Obtener relaciones de hijos
        relationships = get_relationships(pid)
        for rel in relationships:
            if rel['tipo_relacion'] in ['hijo', 'hija']:
                child_id = rel['id_pariente']
                if child_id not in visited:
                    _build_descendants_cache(child_id, depth, current_depth + 1, cache, visited)
    
    # Construir caché de descendientes
    cache = {}
    _build_descendants_cache(person_id, max_generations, 0, cache, set())
    
    # Construir árbol de descendientes
    def _build_descendants_tree(pid: int, depth: int) -> Dict[str, Any]:
        if pid not in cache or depth < 0:
            return {}
            
        person = cache[pid]
        person_node = {
            'id': person['id_persona'],
            'nombres': person['nombres'],
            'apellidos': person['apellidos'],
            'hijos': []
        }
        
        if depth > 0:
            relationships = get_relationships(pid)
            for rel in relationships:
                if rel['tipo_relacion'] in ['hijo', 'hija']:
                    child_tree = _build_descendants_tree(rel['id_pariente'], depth - 1)
                    if child_tree:
                        person_node['hijos'].append(child_tree)
        
        return person_node
    
    return _build_descendants_tree(person_id, max_generations)
