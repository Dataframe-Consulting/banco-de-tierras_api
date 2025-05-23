from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query

from app.config.database import get_db

from app.schemas.auditoria import AuditoriaResponse
from app.services.auditoria import get_all_auditorias

router = APIRouter(prefix="/auditoria", tags=["Auditorias"])

@router.get("/", response_model=List[AuditoriaResponse])
def get_auditorias(
    db: Session = Depends(get_db),
    operacion: Optional[str] = Query(None, description="Busca por operacion..."),
    tabla_afectada: Optional[str] = Query(None, description="Busca por tabla afectada..."),
    usuario_username: Optional[str] = Query(None, description="Busca por usuario..."),
    registrado_desde: Optional[str] = Query(None, description="Fecha desde la que se registró la auditoría..."),
    registrado_hasta: Optional[str] = Query(None, description="Fecha hasta la que se registró la auditoría..."),
):
    return get_all_auditorias(db, operacion, tabla_afectada, usuario_username, registrado_desde, registrado_hasta)