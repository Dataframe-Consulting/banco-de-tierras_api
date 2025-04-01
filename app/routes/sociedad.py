from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.sociedad import SociedadCreate, SociedadResponse, PaginatedSociedadesResponse
from app.services.sociedad import get_all_sociedades, get_all_sociedades_without_pagination, get_sociedad_by_id, get_sociedad_by_porcentaje, create_sociedad, update_sociedad, delete_sociedad

router = APIRouter(prefix="/sociedad", tags=["Sociedades"])

# WITH PAGINATION
# @router.get("/", response_model=PaginatedSociedadesResponse)
# def get_sociedades(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_sociedades(db, page, page_size)

# WITHOUT PAGINATION
@router.get("/", response_model=List[SociedadResponse])
def get_sociedades(db: Session = Depends(get_db)):
    return get_all_sociedades_without_pagination(db)

@router.get("/{sociedad_id}", response_model=SociedadResponse)
def get_sociedad(sociedad_id: int, db: Session = Depends(get_db)):
    db_sociedad = get_sociedad_by_id(db, sociedad_id)
    if not db_sociedad:
        raise HTTPException(status_code=404, detail="Sociedad no encontrada")
    return db_sociedad

@router.post("/", response_model=SociedadResponse)
def create_new_sociedad(sociedad: SociedadCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_sociedad = get_sociedad_by_porcentaje(db, sociedad.porcentaje_participacion)
    if db_sociedad:
        raise HTTPException(status_code=400, detail="La sociedad con este porcentaje ya está registrada")
    return create_sociedad(db, sociedad, user)

@router.put("/{sociedad_id}", response_model=SociedadResponse)
def update_some_sociedad(sociedad_id: int, sociedad: SociedadCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_sociedad = get_sociedad_by_id(db, sociedad_id)
    if not db_sociedad:
        raise HTTPException(status_code=404, detail="Sociedad no encontrada")
    return update_sociedad(db, sociedad_id, sociedad, user)

@router.delete("/{sociedad_id}", response_model=SociedadResponse)
def remove_sociedad(sociedad_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_sociedad = get_sociedad_by_id(db, sociedad_id)
    if not db_sociedad:
        raise HTTPException(status_code=404, detail="Sociedad no encontrada")
    return delete_sociedad(db, sociedad_id, user)