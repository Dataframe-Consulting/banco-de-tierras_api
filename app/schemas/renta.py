from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .propiedad import PropiedadResponse

class RentaBase(BaseModel):
    nombre_comercial: str
    razon_social: str
    renta_sin_iva: float
    meses_deposito_garantia: int
    meses_gracia: int
    meses_gracia_fecha_inicio: Optional[datetime] = None
    meses_gracia_fecha_fin: Optional[datetime] = None
    meses_renta_anticipada: int
    renta_anticipada_fecha_inicio: Optional[datetime] = None
    renta_anticipada_fecha_fin: Optional[datetime] = None
    incremento_mes: str
    incremento_nota: Optional[str] = None
    inicio_vigencia: datetime
    fin_vigencia_forzosa: datetime
    fin_vigencia_no_forzosa: Optional[datetime] = None
    vigencia_nota: Optional[str] = None

class RentaCreate(RentaBase):
    pass

class RentaResponse(RentaBase):
    id: int
    propiedades: List[PropiedadResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedRentasResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[RentaResponse]