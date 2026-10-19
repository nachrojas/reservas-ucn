from pydantic import BaseModel, Field, ConfigDict
from datetime import date, time
from typing import Optional

# --- DTOs para Usuario ---
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: str = Field(..., min_length=5, max_length=120)
    telefono: Optional[str] = Field(default=None, max_length=20)

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- DTOs para Espacio ---
class EspacioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    ubicacion: str = Field(..., min_length=2, max_length=150)
    capacidad: int = Field(..., gt=0)
    disponibilidad_total: bool = True

class EspacioCreate(EspacioBase):
    pass

class EspacioResponse(EspacioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- DTOs para Reserva ---
class ReservaBase(BaseModel):
    usuario_id: int = Field(..., gt=0)
    espacio_id: int = Field(..., gt=0)
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str = Field(default="activa")

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    """Esquema para PATCH: todos los campos son opcionales (modificación parcial)"""
    usuario_id: Optional[int] = Field(default=None, gt=0)
    espacio_id: Optional[int] = Field(default=None, gt=0)
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estado: Optional[str] = None

class ReservaResponse(ReservaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)