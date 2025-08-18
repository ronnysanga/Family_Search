from typing import Dict, List, Optional
from utils.console_utils import clear_screen, show_message, show_header
from services.person.get import get_person_by_user_id, get_person_by_id
from views.person.select_person import select_person
from database import create_connection, close_connection

def get_parents(person_id: int) -> List[Dict]:
    """
    Obtiene los padres directos de una persona.
    """
    conn = create_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT p.id_persona, p.nombres, p.apellidos, rf.tipo_relacion
            FROM relacion_familiar rf
            JOIN persona p ON rf.id_persona1 = p.id_persona
            WHERE rf.id_persona2 = %s 
            AND rf.tipo_relacion IN ('padre', 'madre')
        """, (person_id,))
        
        return cursor.fetchall()
        
    except Exception as e:
        print(f"Error al obtener padres: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        close_connection(conn)

def show_ancestors(person_id: int, level: int = 1) -> None:
    """
    Muestra los ancestros de una persona de forma recursiva.
    """
    parents = get_parents(person_id)
    
    if not parents:
        return
        
    for parent in parents:
        indent = '  ' * level
        print(f"{indent}└── {parent['nombres']} {parent['apellidos']}")
        
        show_ancestors(parent['id_persona'], level + 1)

def show_person_tree(person_id: int, is_current_user: bool = False) -> None:
    """
    Muestra el árbol genealógico de una persona específica.
    """
    clear_screen()
    show_header("ÁRBOL GENEALÓGICO")
    
    person = get_person_by_id(person_id)
    if not person:
        show_message("No se encontró la persona seleccionada.", "error")
        return
    
    relation_note = " (Tú)" if is_current_user else ""
    print(f"\n{person['nombres']} {person['apellidos']}{relation_note}")

    show_ancestors(person_id)

def show_family_tree(user_id: int) -> None:
    """
    Muestra el menú del árbol genealógico con opción de buscar personas.
    """
    while True:
        clear_screen()
        show_header("ÁRBOL GENEALÓGICO")
        
        print("\nOpciones:")
        print("1. Ver mi árbol genealógico")
        print("2. Buscar persona")
        print("3. Volver al menú principal")
        
        choice = input("\nSeleccione una opción: ").strip()
        
        if choice == '1':

            show_person_tree(user_id, is_current_user=True)
            input("\nPresione ENTER para continuar...")
            
        elif choice == '2':

            person = select_person("Seleccione una persona para ver su árbol")
            if person:
                show_person_tree(person['id_persona'])
                input("\nPresione ENTER para continuar...")
                
        elif choice == '3':
            return
            
        else:
            show_message("Opción no válida. Intente nuevamente.", "error")

def get_family_members(person_id: int) -> Dict[str, List[Dict]]:
    """
    Obtiene todos los familiares de una persona.
    Retorna un diccionario con listas de familiares por tipo de relación.
    """
    family = {
        'padres': [],
        'hijos': [],
        'hermanos': [],
        'conyuges': []
    }
    
    try:

        relationships = get_relationships(person_id)
        
        for rel in relationships:
            if not rel or 'id_pariente' not in rel:
                continue
                

            relative = {
                'id_persona': rel['id_pariente'],
                'nombres': rel.get('nombre_pariente', 'Sin nombre').split()[0],
                'apellidos': ' '.join(rel.get('nombre_pariente', 'Sin apellido').split()[1:]),
                'tipo_relacion': rel.get('tipo_relacion', '')
            }
            

            rel_type = rel.get('tipo_relacion', '')
            if rel_type in ['padre', 'madre']:
                family['padres'].append(relative)
            elif rel_type in ['hijo', 'hija']:
                family['hijos'].append(relative)
            elif rel_type in ['esposo', 'esposa']:
                family['conyuges'].append(relative)
            elif rel_type in ['hermano', 'hermana']:
                family['hermanos'].append(relative)
        
        return family
        
    except Exception as e:
        print(f"Error al obtener familiares: {e}")
        return family
