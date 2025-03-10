from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.vocacion_especifica import VocacionEspecificaCreate, VocacionEspecificaResponse, PaginatedVocacionesEspecificasResponse
from app.services.vocacion_especifica import get_all_vocaciones_especificas, get_all_vocaciones_especificas_without_pagination, get_vocacion_especifica_by_id, get_vocacion_especifica_by_valor, create_vocacion_especifica, update_vocacion_especifica, delete_vocacion_especifica

router = APIRouter(prefix="/vocacion_especifica", tags=["Vocaciones Especificas"])

# WITH PAGINATION
# @router.get("/", response_model=PaginatedVocacionesEspecificasResponse)
# def get_vocaciones_especificas(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_vocaciones_especificas(db, page, page_size)

# WITHOUT PAGINATION
@router.get("/", response_model=List[VocacionEspecificaResponse])
def get_vocaciones_especificas(db: Session = Depends(get_db)):
    return get_all_vocaciones_especificas_without_pagination(db)

@router.get("/{vocacion_especifica_id}", response_model=VocacionEspecificaResponse)
def get_vocacion_especifica(vocacion_especifica_id: int, db: Session = Depends(get_db)):
    db_vocacion_especifica = get_vocacion_especifica_by_id(db, vocacion_especifica_id)
    if not db_vocacion_especifica:
        raise HTTPException(status_code=404, detail="Vocación específica no encontrada")
    return db_vocacion_especifica

@router.post("/", response_model=VocacionEspecificaResponse)
def create_new_vocacion(vocacion_especifica: VocacionEspecificaCreate, db: Session = Depends(get_db)):
    db_vocacion_especifica = get_vocacion_especifica_by_valor(db, vocacion_especifica.valor)
    if db_vocacion_especifica:
        raise HTTPException(status_code=400, detail="La vocación específica ya está registrada")
    return create_vocacion_especifica(db, vocacion_especifica)

@router.put("/{vocacion_especifica_id}", response_model=VocacionEspecificaResponse)
def update_some_vocacion(vocacion_especifica_id: int, vocacion_especifica: VocacionEspecificaCreate, db: Session = Depends(get_db)):
    db_vocacion_especifica = get_vocacion_especifica_by_id(db, vocacion_especifica_id)
    if not db_vocacion_especifica:
        raise HTTPException(status_code=404, detail="Vocación específica no encontrada")
    return update_vocacion_especifica(db, vocacion_especifica_id, vocacion_especifica)

@router.delete("/{vocacion_especifica_id}", response_model=VocacionEspecificaResponse)
def remove_vocacion_especifica(vocacion_especifica_id: int, db: Session = Depends(get_db)):
    db_vocacion_especifica = get_vocacion_especifica_by_id(db, vocacion_especifica_id)
    if not db_vocacion_especifica:
        raise HTTPException(status_code=404, detail="Vocación específica no encontrada")
    return delete_vocacion_especifica(db, vocacion_especifica_id)