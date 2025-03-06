from datetime import datetime
from pydantic import BaseModel
from typing import List

class VocacionBase(BaseModel):
    valor: str

class VocacionCreate(VocacionBase):
    pass

class VocacionResponse(VocacionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedVocacionesResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[VocacionResponse]