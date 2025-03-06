from datetime import datetime
from pydantic import BaseModel
from typing import List
from .propiedad import PropiedadResponse

class ProcesoLegalBase(BaseModel):
    abogado: str
    tipo_proceso: str
    estatus: str
    propiedad_id: int

class ProcesoLegalCreate(ProcesoLegalBase):
    pass

class ProcesoLegalResponse(ProcesoLegalBase):
    id: int
    propiedad: PropiedadResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedProcesosLegalesResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[ProcesoLegalResponse]