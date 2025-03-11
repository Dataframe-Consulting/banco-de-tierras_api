from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.proceso_legal import ProcesoLegalCreate, ProcesoLegalResponse, PaginatedProcesosLegalesResponse
from app.services.proceso_legal import get_all_procesos_legales, get_all_procesos_legales_without_pagination, get_proceso_legal_by_id, create_proceso_legal, update_proceso_legal, delete_proceso_legal
from app.services.propiedad import get_propiedad_by_id

router = APIRouter(prefix="/proceso_legal", tags=["Procesos Legales"])

# WITH PAGINATION
# @router.get("/", response_model=PaginatedProcesosLegalesResponse)
# def get_procesos_legales(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_procesos_legales(db, page, page_size)

# WITHOUT PAGINATION
@router.get("/", response_model=List[ProcesoLegalResponse])
def get_procesos_legales(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Busca por abogado..."),
    propiedad_id: Optional[int] = Query(None, description="Filtrar por ID de propiedad")
):
    return get_all_procesos_legales_without_pagination(db, q, propiedad_id)

@router.get("/{proceso_legal_id}", response_model=ProcesoLegalResponse)
def get_proceso_legal(proceso_legal_id: int, db: Session = Depends(get_db)):
    db_proceso_legal = get_proceso_legal_by_id(db, proceso_legal_id)
    if not db_proceso_legal:
        raise HTTPException(status_code=404, detail="Proceso Legal no encontrado")
    return db_proceso_legal

@router.post("/", response_model=ProcesoLegalResponse)
def create_new_proceso_legal(proceso_legal: ProcesoLegalCreate, db: Session = Depends(get_db)):
    db_propiedad = get_propiedad_by_id(db, proceso_legal.propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return create_proceso_legal(db, proceso_legal)

@router.put("/{proceso_legal_id}", response_model=ProcesoLegalResponse)
def update_existing_proceso_legal(proceso_legal_id: int, proceso_legal: ProcesoLegalCreate, db: Session = Depends(get_db)):
    db_proceso_legal = get_proceso_legal_by_id(db, proceso_legal_id)
    if not db_proceso_legal:
        raise HTTPException(status_code=404, detail="Proceso Legal no encontrado")
    db_propiedad = get_propiedad_by_id(db, proceso_legal.propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return update_proceso_legal(db, proceso_legal_id, proceso_legal)

@router.delete("/{proceso_legal_id}", response_model=ProcesoLegalResponse)
def delete_existing_proceso_legal(proceso_legal_id: int, db: Session = Depends(get_db)):
    db_proceso_legal = get_proceso_legal_by_id(db, proceso_legal_id)
    if not db_proceso_legal:
        raise HTTPException(status_code=404, detail="Proceso Legal no encontrado")
    return delete_proceso_legal(db, proceso_legal_id)