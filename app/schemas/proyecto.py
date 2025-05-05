from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .situacion_fisica import SituacionFisicaResponse
from .vocacion import VocacionResponse
from .vocacion_especifica import VocacionEspecificaResponse
from .garantia import GarantiaResponse
from .ubicacion import UbicacionResponse
from .proceso_legal import ProcesoLegalResponse
from .archivo import ArchivoResponse

class PropiedadSimpleResponse(BaseModel):
    id: int
    nombre: str
    superficie: float
    valor_comercial: float
    anio_valor_comercial: Optional[int] = None
    clave_catastral: str
    base_predial: float
    adeudo_predial: Optional[float] = None
    anios_pend_predial: Optional[int] = None
    comentarios: Optional[str] = None
    ubicaciones: List[UbicacionResponse] = []
    garantias: List[GarantiaResponse] = []
    procesos_legales: List[ProcesoLegalResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

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
    propiedades: List[PropiedadSimpleResponse] = []
    archivos: List[ArchivoResponse] = []
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
