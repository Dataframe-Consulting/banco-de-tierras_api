from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .proyecto import ProyectoResponse
from .propietario import PropietarioResponse
from .sociedad import SociedadResponse
from .garantia import GarantiaResponse
from .ubicacion import UbicacionResponse
from .proceso_legal import ProcesoLegalResponse

class RentaSimpleResponse(BaseModel):
    id: int
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
    created_at: datetime
    updated_at: datetime

class PropietarioSociedadPropiedadBase(BaseModel):
    es_socio: bool

class PropietarioSociedadPropiedadCreate(PropietarioSociedadPropiedadBase):
    pass

class PropietarioSociedadPropiedadResponse(PropietarioSociedadPropiedadBase):
    propietario_id: int
    propietario: PropietarioResponse
    sociedad_id: int
    sociedad: SociedadResponse
    propiedad_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PropiedadBase(BaseModel):
    nombre: str
    superficie: float
    valor_comercial: float
    anio_valor_comercial: Optional[int] = None
    clave_catastral: str
    base_predial: float
    adeudo_predial: Optional[float] = None
    anios_pend_predial: Optional[int] = None
    comentarios: Optional[str] = None
    proyecto_id: int

class PropiedadCreate(PropiedadBase):
    pass

class PropiedadResponse(PropiedadBase):
    id: int
    proyecto: ProyectoResponse
    propietarios_sociedades: List[PropietarioSociedadPropiedadResponse] = []
    ubicaciones: List[UbicacionResponse] = []
    garantias: List[GarantiaResponse] = []
    procesos_legales: List[ProcesoLegalResponse] = []
    rentas: List[RentaSimpleResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedPropiedadesResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[PropiedadResponse]