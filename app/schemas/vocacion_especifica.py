from datetime import datetime
from pydantic import BaseModel
from typing import List

class VocacionEspecificaBase(BaseModel):
    valor: str

class VocacionEspecificaCreate(VocacionEspecificaBase):
    pass

class VocacionEspecificaResponse(VocacionEspecificaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedVocacionesEspecificasResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[VocacionEspecificaResponse]