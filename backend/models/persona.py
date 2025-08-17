from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date
from typing import Optional, List
from enum import Enum

class Sexo(str, Enum):
    MASCULINO = "masculino"
    FEMENINO = "femenino"

class PersonaBase(BaseModel):
    nombres: str = Field(..., min_length=2, max_length=100, description="Nombres de la persona")
    apellidos: str = Field(..., min_length=2, max_length=100, description="Apellidos de la persona")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento (YYYY-MM-DD)")
    fecha_defuncion: Optional[date] = Field(None, description="Fecha de fallecimiento (opcional, YYYY-MM-DD)")
    sexo: Sexo = Field(..., description="Sexo de la persona")
    lugar_nacimiento: Optional[str] = Field(None, max_length=225, description="Lugar de nacimiento")
    lugar_defuncion: Optional[str] = Field(None, max_length=225, description="Lugar de fallecimiento")
    biografia: Optional[str] = Field(None, description="Biografía o notas adicionales")

    @field_validator('fecha_defuncion')
    def validate_fechas(cls, v, values):
        if 'fecha_nacimiento' in values and v is not None and values['fecha_nacimiento'] is not None:
            if v < values['fecha_nacimiento']:
                raise ValueError('La fecha de defunción no puede ser anterior a la fecha de nacimiento')
        return v

class PersonaCreate(PersonaBase):
    id_usuario_creador: int = Field(..., description="ID del usuario que crea el registro")

class PersonaUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    fecha_nacimiento: Optional[date] = None
    fecha_defuncion: Optional[date] = None
    sexo: Optional[Sexo] = None
    lugar_nacimiento: Optional[str] = None
    lugar_defuncion: Optional[str] = None
    biografia: Optional[str] = None

class PersonaResponse(PersonaBase):
    id_persona: int
    fecha_creacion: date
    fecha_actualizacion: Optional[date] = None

    class Config:
        from_attributes = True

class RelacionTipo(str, Enum):
    PADRE = "padre"
    MADRE = "madre"
    HIJO = "hijo"
    HIJA = "hija"
    ESPOSO = "esposo"
    ESPOSA = "esposa"
    HERMANO = "hermano"
    HERMANA = "hermana"

class RelacionFamiliarCreate(BaseModel):
    id_persona1: int = Field(..., description="ID de la persona origen")
    id_persona2: int = Field(..., description="ID de la persona destino")
    tipo_relacion: RelacionTipo = Field(..., description="Tipo de relación entre las personas")
    id_usuario_creador: int = Field(..., description="ID del usuario que crea la relación")

class RelacionFamiliarResponse(RelacionFamiliarCreate):
    id_relacion: int
    fecha_creacion: date

    class Config:
        from_attributes = True
