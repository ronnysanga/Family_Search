from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import date
import mysql.connector
from mysql.connector import Error
import logging

from models.persona import (
    PersonaCreate, 
    PersonaResponse, 
    PersonaUpdate,
    RelacionFamiliarCreate,
    RelacionFamiliarResponse,
    RelacionTipo
)
from config.database import get_db_connection

router = APIRouter(
    prefix="/api/personas",
    tags=["personas"],
    responses={404: {"description": "Not found"}},
)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_query(query: str, params: tuple = None, fetch_one: bool = False):
    """
    Ejecuta una consulta SQL y devuelve el resultado.
    """
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE')):
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()
        else:
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        logger.error(f"Error en la consulta SQL: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

# Endpoints para Personas
@router.post("/", response_model=PersonaResponse, status_code=201)
async def crear_persona(persona: PersonaCreate):
    """
    Crea una nueva persona en la base de datos.
    """
    query = """
    INSERT INTO persona (
        id_usuario_creador, nombres, apellidos, fecha_nacimiento, 
        fecha_defuncion, sexo, lugar_nacimiento, lugar_defuncion, biografia
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        persona.id_usuario_creador, persona.nombres, persona.apellidos, 
        persona.fecha_nacimiento, persona.fecha_defuncion, persona.sexo.value,
        persona.lugar_nacimiento, persona.lugar_defuncion, persona.biografia
    )
    
    try:
        persona_id = execute_query(query, params)
        # Obtener la persona recién creada
        return obtener_persona_por_id(persona_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error al crear persona: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear la persona: {str(e)}")

@router.get("/{persona_id}", response_model=PersonaResponse)
async def obtener_persona(persona_id: int):
    """
    Obtiene una persona por su ID.
    """
    return obtener_persona_por_id(persona_id)

def obtener_persona_por_id(persona_id: int):
    """
    Función auxiliar para obtener una persona por ID.
    """
    query = """
    SELECT 
        id_persona, id_usuario_creador, nombres, apellidos, 
        fecha_nacimiento, fecha_defuncion, sexo, lugar_nacimiento, 
        lugar_defuncion, biografia, fecha_creacion, fecha_actualizacion
    FROM persona 
    WHERE id_persona = %s
    """
    persona = execute_query(query, (persona_id,), fetch_one=True)
    
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    return persona

@router.put("/{persona_id}", response_model=PersonaResponse)
async def actualizar_persona(persona_id: int, persona_update: PersonaUpdate):
    """
    Actualiza los datos de una persona existente.
    """
    # Verificar si la persona existe
    obtener_persona_por_id(persona_id)
    
    # Construir la consulta dinámicamente basada en los campos proporcionados
    update_fields = []
    params = []
    
    for field, value in persona_update.dict(exclude_unset=True).items():
        if field == 'sexo' and value is not None:
            value = value.value
        update_fields.append(f"{field} = %s")
        params.append(value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar")
    
    # Agregar el ID al final para la condición WHERE
    params.append(persona_id)
    
    query = f"""
    UPDATE persona 
    SET {', '.join(update_fields)}, fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id_persona = %s
    """
    
    try:
        execute_query(query, tuple(params))
        return obtener_persona_por_id(persona_id)
    except Exception as e:
        logger.error(f"Error al actualizar persona: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar la persona: {str(e)}")

@router.delete("/{persona_id}", status_code=204)
async def eliminar_persona(persona_id: int):
    """
    Elimina una persona y todas sus relaciones familiares.
    """
    # Verificar si la persona existe
    obtener_persona_por_id(persona_id)
    
    # Nota: Las relaciones se eliminarán en cascada debido a la configuración de la FK
    query = "DELETE FROM persona WHERE id_persona = %s"
    
    try:
        execute_query(query, (persona_id,))
        return None
    except Exception as e:
        logger.error(f"Error al eliminar persona: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar la persona: {str(e)}")

# Endpoints para Relaciones Familiares
@router.post("/relaciones/", response_model=RelacionFamiliarResponse, status_code=201)
async def crear_relacion_familiar(relacion: RelacionFamiliarCreate):
    """
    Crea una nueva relación familiar entre dos personas.
    """
    # Verificar que las personas existan
    obtener_persona_por_id(relacion.id_persona1)
    obtener_persona_por_id(relacion.id_persona2)
    
    query = """
    INSERT INTO relacion_familiar 
    (id_persona1, id_persona2, tipo_relacion, id_usuario_creador)
    VALUES (%s, %s, %s, %s)
    """
    params = (
        relacion.id_persona1, 
        relacion.id_persona2, 
        relacion.tipo_relacion.value,
        relacion.id_usuario_creador
    )
    
    try:
        relacion_id = execute_query(query, params)
        # Obtener la relación recién creada
        return obtener_relacion_por_id(relacion_id)
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=400, 
                detail="Ya existe una relación idéntica entre estas personas"
            )
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error al crear relación familiar: {e}")
        raise HTTPException(status_code=500, detail=f"Error al crear la relación familiar: {str(e)}")

def obtener_relacion_por_id(relacion_id: int):
    """
    Función auxiliar para obtener una relación por ID.
    """
    query = """
    SELECT id_relacion, id_persona1, id_persona2, tipo_relacion, 
           id_usuario_creador, fecha_creacion
    FROM relacion_familiar 
    WHERE id_relacion = %s
    """
    relacion = execute_query(query, (relacion_id,), fetch_one=True)
    
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    return relacion

@router.get("/{persona_id}/familiares/", response_model=List[dict])
async def obtener_familiares(
    persona_id: int,
    tipo_relacion: Optional[RelacionTipo] = None,
    incluir_ascendientes: bool = False,
    incluir_descendientes: bool = True,
    max_nivel: int = 3
):
    """
    Obtiene los familiares de una persona con opciones de filtrado.
    """
    # Verificar que la persona existe
    obtener_persona_por_id(persona_id)
    
    # Construir la consulta base
    query = """
    SELECT 
        p.id_persona, p.nombres, p.apellidos, p.fecha_nacimiento,
        p.sexo, rf.tipo_relacion
    FROM relacion_familiar rf
    JOIN persona p ON 
    """
    
    # Determinar la dirección de la relación
    if incluir_ascendientes and not incluir_descendientes:
        query += "p.id_persona = rf.id_persona1 WHERE rf.id_persona2 = %s"
    else:
        # Por defecto, buscar descendientes
        query += "p.id_persona = rf.id_persona2 WHERE rf.id_persona1 = %s"
    
    params = [persona_id]
    
    # Filtrar por tipo de relación si se especifica
    if tipo_relacion:
        query += " AND rf.tipo_relacion = %s"
        params.append(tipo_relacion.value)
    
    # Limitar el número de resultados para evitar sobrecarga
    query += " LIMIT 100"
    
    try:
        return execute_query(query, tuple(params))
    except Exception as e:
        logger.error(f"Error al obtener familiares: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener los familiares: {str(e)}")

@router.get("/reportes/arbol-genealogico/")
async def generar_reporte_arbol_genealogico(
    persona_id: int = Query(..., description="ID de la persona raíz del árbol"),
    niveles: int = Query(3, ge=1, le=5, description="Niveles de profundidad del árbol")
):
    """
    Genera un reporte del árbol genealógico de una persona.
    """
    # Verificar que la persona existe
    obtener_persona_por_id(persona_id)
    
    # Esta es una implementación simplificada
    # En una aplicación real, podrías usar una consulta recursiva o un procedimiento almacenado
    query = """
    WITH RECURSIVE arbol AS (
        -- Caso base: la persona raíz
        SELECT id_persona, nombres, apellidos, 0 as nivel
        FROM persona 
        WHERE id_persona = %s
        
        UNION ALL
        
        -- Obtener relaciones directas
        SELECT p.id_persona, p.nombres, p.apellidos, a.nivel + 1
        FROM arbol a
        JOIN relacion_familiar rf ON 
            (a.id_persona = rf.id_persona1 OR a.id_persona = rf.id_persona2)
        JOIN persona p ON 
            (p.id_persona = rf.id_persona1 OR p.id_persona = rf.id_persona2) 
            AND p.id_persona != a.id_persona
        WHERE a.nivel < %s
    )
    SELECT DISTINCT id_persona, nombres, apellidos, nivel
    FROM arbol
    ORDER BY nivel, apellidos, nombres
    """
    
    try:
        return execute_query(query, (persona_id, niveles))
    except Exception as e:
        logger.error(f"Error al generar árbol genealógico: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar el árbol genealógico: {str(e)}")

@router.get("/reportes/estadisticas/")
async def generar_estadisticas():
    """
    Genera estadísticas generales sobre las personas y relaciones en la base de datos.
    """
    query = """
    -- Conteo total de personas
    SELECT 'total_personas' as tipo, COUNT(*) as cantidad FROM persona
    UNION ALL
    -- Conteo por sexo
    SELECT CONCAT('total_', sexo) as tipo, COUNT(*) as cantidad 
    FROM persona 
    GROUP BY sexo
    UNION ALL
    -- Conteo de relaciones por tipo
    SELECT CONCAT('total_relaciones_', tipo_relacion) as tipo, COUNT(*) as cantidad
    FROM relacion_familiar
    GROUP BY tipo_relacion
    """
    
    try:
        resultados = execute_query(query)
        return {item['tipo']: item['cantidad'] for item in resultados}
    except Exception as e:
        logger.error(f"Error al generar estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error al generar las estadísticas: {str(e)}")
