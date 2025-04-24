from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .proyecto import ProyectoResponse
from .propietario import PropietarioResponse
from .garantia import GarantiaResponse
from .ubicacion import UbicacionResponse
from .proceso_legal import ProcesoLegalResponse

class RentaSimpleResponse(BaseModel):
    id: int
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
    created_at: datetime
    updated_at: datetime

class PropietarioPropiedadBase(BaseModel):
    es_socio: bool
    sociedad_porcentaje_participacion: float

class PropietarioPropiedadCreate(PropietarioPropiedadBase):
    pass

class PropietarioPropiedadResponse(PropietarioPropiedadBase):
    propietario_id: int
    propietario: PropietarioResponse
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
    propietarios: List[PropietarioPropiedadResponse] = []
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