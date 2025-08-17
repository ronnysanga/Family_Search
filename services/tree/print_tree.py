"""
Print Tree Module

This module provides functions for printing family tree visualizations.
"""
from typing import Dict, Any
from .get_family_tree import get_family_tree
from utils.console_utils import show_message

def _print_node(node: Dict[str, Any], level: int = 0, prefix: str = '') -> None:
    """
    Recursively print a node and its children in the family tree.
    
    Args:
        node: The current node to print
        level: Current depth level in the tree (for indentation)
        prefix: Prefix for the current node (for tree visualization)
    """
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

def print_family_tree(person_id: int, max_depth: int = 3) -> None:
    """
    Print a text-based representation of a family tree.
    
    Args:
        person_id: ID of the root person
        max_depth: Maximum depth to display (default: 3)
    """
    # Start building the tree from the root person
    tree = get_family_tree(person_id, max_depth)
    if tree:
        _print_node(tree)
    else:
        show_message("No se pudo generar el árbol genealógico.", "error")
