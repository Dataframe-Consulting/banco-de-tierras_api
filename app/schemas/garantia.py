from typing import List
from datetime import datetime
from pydantic import BaseModel

class GarantiBase(BaseModel):
    beneficiario: str
    monto: float
    fecha_inicio: datetime
    fecha_fin: datetime

class GarantiaCreate(GarantiBase):
    pass

class GarantiaResponse(GarantiBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedGarantiasResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[GarantiaResponse]