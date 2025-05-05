from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .archivo import ArchivoResponse

class ProcesoLegalBase(BaseModel):
    abogado: str
    tipo_proceso: str
    estatus: str
    comentarios: Optional[str] = None

class ProcesoLegalCreate(ProcesoLegalBase):
    pass

class ProcesoLegalResponse(ProcesoLegalBase):
    id: int
    archivos: List[ArchivoResponse] = []
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