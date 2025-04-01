from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.situacion_fisica import SituacionFisicaCreate, SituacionFisicaResponse, PaginatedSituacionesFisicasResponse
from app.services.situacion_fisica import get_all_situaciones_fisicas, get_all_situaciones_fisicas_without_pagination, get_situacion_fisica_by_id, get_situacion_fisica_by_nombre, create_situacion_fisica, update_situacion_fisica, delete_situacion_fisica

router = APIRouter(prefix="/situacion_fisica", tags=["Situaciones Físicas"])

# WITHOUT PAGINATION
# @router.get("/", response_model=PaginatedSituacionesFisicasResponse)
# def get_situaciones_fisicas(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_situaciones_fisicas(db, page, page_size)

# WITH PAGINATION
@router.get("/", response_model=List[SituacionFisicaResponse])
def get_situaciones_fisicas(db: Session = Depends(get_db)):
    return get_all_situaciones_fisicas_without_pagination(db)

@router.get("/{situacion_fisica_id}", response_model=SituacionFisicaResponse)
def get_situacion_fisica(situacion_fisica_id: int, db: Session = Depends(get_db)):
    db_situacion_fisica = get_situacion_fisica_by_id(db, situacion_fisica_id)
    if not db_situacion_fisica:
        raise HTTPException(status_code=404, detail="Situación Física no encontrada")
    return db_situacion_fisica

@router.post("/", response_model=SituacionFisicaResponse)
def create_new_situacion_fisica(situacion_fisica: SituacionFisicaCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_situacion_fisica = get_situacion_fisica_by_nombre(db, situacion_fisica.nombre)
    if db_situacion_fisica:
        raise HTTPException(status_code=400, detail="La Situación Física ya está registrada")
    return create_situacion_fisica(db, situacion_fisica, user)

@router.put("/{situacion_fisica_id}", response_model=SituacionFisicaResponse)
def update_some_situacion_fisica(situacion_fisica_id: int, situacion_fisica: SituacionFisicaCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_situacion_fisica = get_situacion_fisica_by_id(db, situacion_fisica_id)
    if not db_situacion_fisica:
        raise HTTPException(status_code=404, detail="Situación Física no encontrada")
    return update_situacion_fisica(db, situacion_fisica_id, situacion_fisica, user)

@router.delete("/{situacion_fisica_id}", response_model=SituacionFisicaResponse)
def remove_situacion_fisica(situacion_fisica_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_situacion_fisica = get_situacion_fisica_by_id(db, situacion_fisica_id)
    if not db_situacion_fisica:
        raise HTTPException(status_code=404, detail="Situación Física no encontrada")
    return delete_situacion_fisica(db, situacion_fisica_id, user)