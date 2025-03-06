from datetime import datetime
from pydantic import BaseModel

class SociedadBase(BaseModel):
    porcentaje_participacion: float

class SociedadCreate(SociedadBase):
    pass

class SociedadResponse(SociedadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedSociedadesResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: list[SociedadResponse]