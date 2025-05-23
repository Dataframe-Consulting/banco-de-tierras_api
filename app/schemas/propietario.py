from datetime import datetime
from pydantic import BaseModel
from typing import List
from .archivo import ArchivoResponse

class PropietarioBase(BaseModel):
    nombre: str
    rfc: str

class PropietarioCreate(PropietarioBase):
    pass

class PropietarioResponse(PropietarioBase):
    id: int
    archivos: List[ArchivoResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedPropietariosResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[PropietarioResponse]
