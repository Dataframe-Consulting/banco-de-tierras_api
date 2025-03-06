from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .proyecto import ProyectoResponse
from .ubicacion import UbicacionResponse

class PropiedadBase(BaseModel):
    nombre: str
    superficie: float
    valor_comercial: float
    anio_valor_comercial: Optional[int] = None
    clave_catastral: str
    base_predial: float
    adeudo_predial: Optional[float] = None
    anios_pend_predial: Optional[int] = None
    comentarios: Optional[str] = None
    proyecto_id: int

class PropiedadCreate(PropiedadBase):
    pass

class PropiedadResponse(PropiedadBase):
    id: int
    proyecto: ProyectoResponse
    ubicaciones: List[UbicacionResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedPropiedadesResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[PropiedadResponse]