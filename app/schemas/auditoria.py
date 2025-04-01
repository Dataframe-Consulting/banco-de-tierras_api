from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AuditoriaBase(BaseModel):
    operacion: str
    tabla_afectada: str
    registro_tabla_id: int
    usuario_username: str
    valores_anteriores: Optional[dict] = {}
    valores_nuevos: Optional[dict] = {}

class AuditoriaCreate(AuditoriaBase):
    pass

class AuditoriaResponse(AuditoriaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True