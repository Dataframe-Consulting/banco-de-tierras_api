from datetime import datetime
from pydantic import BaseModel

class SituacionFisicaBase(BaseModel):
    nombre: str

class SituacionFisicaCreate(SituacionFisicaBase):
    pass

class SituacionFisicaResponse(SituacionFisicaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedSituacionesFisicasResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: list[SituacionFisicaResponse]