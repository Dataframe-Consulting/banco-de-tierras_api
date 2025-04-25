from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .propiedad import PropiedadResponse

class RentaBase(BaseModel):
    nombre_comercial: Optional[str] = None
    razon_social: Optional[str] = None
    renta_sin_iva: Optional[float] = None
    meses_deposito_garantia: Optional[int] = None
    meses_gracia: Optional[int] = None
    meses_gracia_fecha_inicio: Optional[datetime] = None
    meses_gracia_fecha_fin: Optional[datetime] = None
    meses_renta_anticipada: Optional[int] = None
    renta_anticipada_fecha_inicio: Optional[datetime] = None
    renta_anticipada_fecha_fin: Optional[datetime] = None
    incremento_mes: Optional[str] = None
    incremento_nota: Optional[str] = None
    inicio_vigencia: Optional[datetime] = None
    fin_vigencia_forzosa: Optional[datetime] = None
    fin_vigencia_no_forzosa: Optional[datetime] = None
    vigencia_nota: Optional[str] = None
    esta_disponible: bool = False
    metros_cuadrados_rentados: Optional[float] = None

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