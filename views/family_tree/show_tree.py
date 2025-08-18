from typing import Dict, List, Tuple
from utils.console_utils import clear_screen, show_message
from services.person.get import get_person_by_user_id
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
        
        # Buscar padres (donde la persona es el hijo)
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

def show_family_tree(user_id: int) -> None:
    """
    Muestra el árbol genealógico ascendente del usuario.
    """
    clear_screen()
    print("\n=== ÁRBOL GENEALÓGICO ===\n")
    
    # Obtener la persona principal (usuario actual)
    person = get_person_by_user_id(user_id)
    if not person:
        show_message("No se encontró su perfil de persona.", "error")
        input("\nPresione ENTER para continuar...")
        return
    
    # Mostrar la persona principal
    print(f"\n{person['nombres']} {person['apellidos']} (Tú)")
    
    # Obtener y mostrar padres
    parents = get_parents(person['id_persona'])
    
    if not parents:
        print("\nNo se encontraron padres registrados.")
        print("Puede agregar padres/madres desde la opción 'Gestionar relaciones familiares'.")
    else:
        print("\nPadres:")
        for parent in parents:
            relation = 'Padre' if parent['tipo_relacion'] == 'padre' else 'Madre'
            print(f"- {parent['nombres']} {parent['apellidos']} ({relation})")
            
            # Mostrar abuelos (padres de los padres)
            grandparents = get_parents(parent['id_persona'])
            if grandparents:
                print("  Abuelos:")
                for grandparent in grandparents:
                    relation = 'Abuelo' if grandparent['tipo_relacion'] == 'padre' else 'Abuela'
                    print(f"  - {grandparent['nombres']} {grandparent['apellidos']} ({relation})")
    
    input("\nPresione ENTER para volver al menú principal...")

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
        # Obtener relaciones donde la persona es person1 (relaciones salientes)
        relationships = get_relationships(person_id)
        
        for rel in relationships:
            if not rel or 'id_pariente' not in rel:
                continue
                
            # Crear un diccionario con la información del familiar
            relative = {
                'id_persona': rel['id_pariente'],
                'nombres': rel.get('nombre_pariente', 'Sin nombre').split()[0],
                'apellidos': ' '.join(rel.get('nombre_pariente', 'Sin apellido').split()[1:]),
                'tipo_relacion': rel.get('tipo_relacion', '')
            }
            
            # Clasificar por tipo de relación
            rel_type = rel.get('tipo_relacion', '')
            if rel_type in ['padre', 'madre']:
                family['padres'].append(relative)
            elif rel_type in ['hijo', 'hija']:
                family['hijos'].append(relative)
            elif rel_type in ['esposo', 'esposa']:
                family['conyuges'].append(relative)
            elif rel_type in ['hermano', 'hermana']:
                family['hermanos'].append(relative)
        
        # Para relaciones donde la persona es person2 (relaciones entrantes)
        # Necesitaríamos una función get_relationships_where_person2
        # Por ahora, manejamos las relaciones inversas en la lógica de agregar relaciones
        
        return family
        
    except Exception as e:
        print(f"Error al obtener familiares: {e}")
        return family
