from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .proyecto import ProyectoResponse
from .sociedad import SociedadResponse
from .garantia import GarantiaResponse
from .ubicacion import UbicacionResponse
from .proceso_legal import ProcesoLegalResponse

class SociedadPropiedadResponse(BaseModel):
    id: int
    sociedad_id: int
    sociedad: SociedadResponse
    propiedad_id: int
    created_at: datetime

    class Config:
        from_attributes = True

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
    sociedades: List[SociedadPropiedadResponse] = []
    ubicaciones: List[UbicacionResponse] = []
    garantias: List[GarantiaResponse] = []
    procesos_legales: List[ProcesoLegalResponse] = []
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