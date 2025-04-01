from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.socio import SocioCreate, SocioResponse, PaginatedSociosResponse
from app.services.socio import get_all_socios, get_all_socios_without_pagination, get_socio_by_id, create_socio, update_socio, delete_socio

router = APIRouter(prefix="/socio", tags=["Socios"])

# WITH PAGINATION
# @router.get("/", response_model=PaginatedSociosResponse)
# def get_socios(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_socios(db, page, page_size)

# WITHOUT PAGINATION
@router.get("/", response_model=List[SocioResponse])
def get_socios(db: Session = Depends(get_db)):
    return get_all_socios_without_pagination(db)

@router.get("/{socio_id}", response_model=SocioResponse)
def get_socio(socio_id: int, db: Session = Depends(get_db)):
    db_socio = get_socio_by_id(db, socio_id)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return db_socio

@router.post("/", response_model=SocioResponse)
def create_new_socio(socio: SocioCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_socio(db, socio, user)

@router.put("/{socio_id}", response_model=SocioResponse)
def update_some_socio(socio_id: int, socio: SocioCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_socio = get_socio_by_id(db, socio_id)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return update_socio(db, socio_id, socio, user)

@router.delete("/{socio_id}", response_model=SocioResponse)
def remove_socio(socio_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_socio = get_socio_by_id(db, socio_id)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return delete_socio(db, socio_id, user)