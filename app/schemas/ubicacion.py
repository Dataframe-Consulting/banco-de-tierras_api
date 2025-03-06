from datetime import datetime
from pydantic import BaseModel
from typing import List

class UbicacionBase(BaseModel):
    nombre: str

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionResponse(UbicacionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedUbicacionesResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[UbicacionResponse]