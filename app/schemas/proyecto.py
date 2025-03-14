from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .situacion_fisica import SituacionFisicaResponse
from .vocacion import VocacionResponse
from .vocacion_especifica import VocacionEspecificaResponse
from .propietario import PropietarioResponse
# from .sociedad import SociedadResponse

# class SociedadProyectoBase(BaseModel):
#     valor: float

# class SociedadProyectoCreate(SociedadProyectoBase):
#     pass

# class SociedadProyectoResponse(SociedadProyectoBase):
#     sociedad_id: int
#     proyecto_id: int
#     sociedad: SociedadResponse
#     created_at: datetime

#     class Config:
#         from_attributes = True

class ProyectoBase(BaseModel):
    nombre: str
    superficie_total: float
    esta_activo: Optional[bool] = True
    comentarios: Optional[str] = None
    situacion_fisica_id: int
    vocacion_id: int
    vocacion_especifica_id: int

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoResponse(ProyectoBase):
    id: int
    situacion_fisica: SituacionFisicaResponse
    vocacion: VocacionResponse
    vocacion_especifica: VocacionEspecificaResponse
    propietarios: List[PropietarioResponse] = []
    # sociedades: List[SociedadProyectoResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedProyectosResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[ProyectoResponse]