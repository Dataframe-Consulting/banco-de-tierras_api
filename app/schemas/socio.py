from datetime import datetime
from pydantic import BaseModel
from typing import List

class SocioBase(BaseModel):
    nombre: str

class SocioCreate(SocioBase):
    pass

class SocioResponse(SocioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedSociosResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[SocioResponse]