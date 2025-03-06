from sqlalchemy.orm import Session
from app.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.vocacion import VocacionCreate, VocacionResponse, PaginatedVocacionesResponse
from app.services.vocacion import get_all_vocaciones, get_vocacion_by_id, get_vocacion_by_valor, create_vocacion, update_vocacion, delete_vocacion

router = APIRouter(prefix="/vocacion", tags=["Vocaciones"])

@router.get("/", response_model=PaginatedVocacionesResponse)
def get_vocaciones(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    return get_all_vocaciones(db, page, page_size)

@router.get("/{vocacion_id}", response_model=VocacionResponse)
def get_vocacion(vocacion_id: int, db: Session = Depends(get_db)):
    db_vocacion = get_vocacion_by_id(db, vocacion_id)
    if not db_vocacion:
        raise HTTPException(status_code=404, detail="Vocacion no encontrada")
    return db_vocacion

@router.post("/", response_model=VocacionResponse)
def create_new_vocacion(vocacion: VocacionCreate, db: Session = Depends(get_db)):
    db_vocacion = get_vocacion_by_valor(db, vocacion.valor)
    if db_vocacion:
        raise HTTPException(status_code=400, detail="La vocacion ya está registrada")
    return create_vocacion(db, vocacion)

@router.put("/{vocacion_id}", response_model=VocacionResponse)
def update_some_vocacion(vocacion_id: int, vocacion: VocacionCreate, db: Session = Depends(get_db)):
    db_vocacion = get_vocacion_by_id(db, vocacion_id)
    if not db_vocacion:
        raise HTTPException(status_code=404, detail="Vocacion no encontrada")
    return update_vocacion(db, vocacion_id, vocacion)

@router.delete("/{vocacion_id}", response_model=VocacionResponse)
def remove_vocacion(vocacion_id: int, db: Session = Depends(get_db)):
    db_vocacion = get_vocacion_by_id(db, vocacion_id)
    if not db_vocacion:
        raise HTTPException(status_code=404, detail="Vocacion no encontrada")
    return delete_vocacion(db, vocacion_id)