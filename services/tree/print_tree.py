"""
Módulo de Visualización de Árbol Genealógico

Este módulo proporciona funciones para visualizar árboles genealógicos
de manera jerárquica y legible.
"""
from typing import Dict, Any, List, Optional
from .get_family_tree import get_family_tree, get_ancestors, get_descendants
from utils.console_utils import show_message, print_colored

def _format_person_info(person: Dict[str, Any], highlight: bool = False) -> str:
    """
    Formatea la información de una persona para mostrarla en el árbol.
    
    Args:
        person: Diccionario con los datos de la persona
        highlight: Si es True, resalta el nombre de la persona
        
    Returns:
        Cadena formateada con la información de la persona
    """
    if not person:
        return ""
        
    name = f"{person['nombres']} {person['apellidos']}"
    birth = f" ({person.get('fecha_nacimiento', '')})" if person.get('fecha_nacimiento') else ""
    
    if highlight:
        return f"\033[1;34m{name}\033[0m{birth}"
    return f"{name}{birth}"

def _print_ancestors(person: Dict[str, Any], level: int = 0) -> None:
    """
    Imprime recursivamente los ancestros de una persona.
    
    Args:
        person: Diccionario con los datos de la persona
        level: Nivel actual de anidamiento (para la indentación)
    """
    if not person:
        return
        
    indent = '│   ' * level
    
    # Imprimir padre
    if person.get('padre'):
        print(f"{indent}├─ Padre: {_format_person_info(person['padre'])}")
        _print_ancestors(person['padre'], level + 1)
    
    # Imprimir madre
    if person.get('madre'):
        print(f"{indent}└─ Madre: {_format_person_info(person['madre'])}")
        _print_ancestors(person['madre'], level + 1)

def _print_descendants(person: Dict[str, Any], level: int = 0, is_last: bool = True) -> None:
    """
    Imprime recursivamente los descendientes de una persona.
    
    Args:
        person: Diccionario con los datos de la persona
        level: Nivel actual de anidamiento (para la indentación)
        is_last: Indica si es el último hijo en la lista
    """
    if not person or 'hijos' not in person:
        return
        
    indent = '    ' * level
    connector = '└─ ' if is_last else '├─ '
    
    for i, child in enumerate(person['hijos']):
        is_last_child = i == len(person['hijos']) - 1
        child_indent = '    ' if is_last_child else '│   '
        
        # Imprimir información del hijo
        print(f"{indent}{connector if i == 0 else child_indent}└─ {_format_person_info(child, True)}")
        
        # Imprimir cónyuges del hijo
        if child.get('esposos'):
            for spouse in child['esposos']:
                print(f"{indent}{child_indent}   ├─ Cónyuge: {_format_person_info(spouse)}")
        
        # Imprimir hermanos del hijo (solo una vez)
        if i == 0 and child.get('hermanos'):
            print(f"{indent}{child_indent}   └─ Hermanos:")
            for sibling in child['hermanos']:
                print(f"{indent}{child_indent}      └─ {_format_person_info(sibling)}")
        
        # Llamada recursiva para los hijos
        _print_descendants(child, level + 1, is_last_child)

def print_family_tree(person_id: int, max_depth: int = 3) -> None:
    """
    Imprime un árbol genealógico completo de una persona.
    
    Args:
        person_id: ID de la persona raíz del árbol
        max_depth: Profundidad máxima del árbol (por defecto: 3)
    """
    # Obtener el árbol genealógico
    tree = get_family_tree(person_id, max_depth)
    if not tree:
        show_message("No se pudo generar el árbol genealógico.", "error")
        return
    
    # Imprimir encabezado
    print("\n" + "=" * 80)
    print(f"ÁRBOL GENEALÓGICO DE {tree['nombres'].upper()} {tree['apellidos'].upper()}".center(80))
    print("=" * 80 + "\n")
    
    # Imprimir ancestros (si los hay)
    if tree.get('padre') or tree.get('madre'):
        print("\nANCESTROS:")
        _print_ancestors(tree)
    
    # Imprimir persona central
    print("\n" + "-" * 80)
    print(f"PERSONA CENTRAL: {_format_person_info(tree, True)}")
    
    # Imprimir cónyuges (si los hay)
    if tree.get('esposos'):
        print("\nCÓNYUGES:")
        for i, spouse in enumerate(tree['esposos'], 1):
            print(f"  {i}. {_format_person_info(spouse)}")
    
    # Imprimir hermanos (si los hay)
    if tree.get('hermanos'):
        print("\nHERMANOS:")
        for i, sibling in enumerate(tree['hermanos'], 1):
            print(f"  {i}. {_format_person_info(sibling)}")
    
    # Imprimir descendientes
    if tree.get('hijos'):
        print("\nDESCENDIENTES:")
        _print_descendants(tree)
    
    print("\n" + "=" * 80)

def print_ancestors_tree(person_id: int, max_generations: int = 3) -> None:
    """
    Imprime solo los ancestros de una persona en formato de árbol.
    
    Args:
        person_id: ID de la persona
        max_generations: Número máximo de generaciones a mostrar
    """
    tree = get_ancestors(person_id, max_generations)
    if not tree:
        show_message("No se pudo generar el árbol de ancestros.", "error")
        return
    
    print("\n" + "=" * 80)
    print(f"ÁRBOL DE ANCESTROS DE {tree['nombres'].upper()} {tree['apellidos'].upper()}".center(80))
    print("=" * 80 + "\n")
    
    _print_ancestors(tree)
    print("\n" + "=" * 80)

def print_descendants_tree(person_id: int, max_generations: int = 3) -> None:
    """
    Imprime solo los descendientes de una persona en formato de árbol.
    
    Args:
        person_id: ID de la persona
        max_generations: Número máximo de generaciones a mostrar
    """
    tree = get_descendants(person_id, max_generations)
    if not tree:
        show_message("No se pudo generar el árbol de descendientes.", "error")
        return
    
    print("\n" + "=" * 80)
    print(f"ÁRBOL DE DESCENDIENTES DE {tree['nombres'].upper()} {tree['apellidos'].upper()}".center(80))
    print("=" * 80 + "\n")
    
    print(f"{_format_person_info(tree, True)}\n")
    _print_descendants(tree)
    print("\n" + "=" * 80)
