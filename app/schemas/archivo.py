from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ArchivoBase(BaseModel):
    url: str

class ArchivoCreate(ArchivoBase):
    pass

class ArchivoResponse(ArchivoBase):
    id: int
    proyecto_id: Optional[int] = None
    propiedad_id: Optional[int] = None
    propietario_id: Optional[int] = None
    garantia_id: Optional[int] = None
    proceso_legal_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True