from typing import List
from sqlalchemy.orm import Session
from app.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException

from app.models.user import User
from app.utils.auth import get_current_user

from app.schemas.propietario import PropietarioCreate, PropietarioResponse
from app.services.propietario import get_all_propietarios_without_pagination, get_propietario_by_id, get_propietario_by_rfc, create_propietario, update_propietario, delete_propietario

router = APIRouter(prefix="/propietario", tags=["Propietarios"])

@router.get("/", response_model=List[PropietarioResponse])
def get_propietarios(db: Session = Depends(get_db)):
    return get_all_propietarios_without_pagination(db)

@router.get("/{propietario_id}", response_model=PropietarioResponse)
def get_propietario(propietario_id: int, db: Session = Depends(get_db)):
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return db_propietario

@router.post("/", response_model=PropietarioResponse)
def create_new_propietario(propietario: PropietarioCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propietario = get_propietario_by_rfc(db, propietario.rfc)
    if db_propietario:
        raise HTTPException(status_code=400, detail="El RFC ya está registrado")
    return create_propietario(db, propietario, user)

@router.put("/{propietario_id}", response_model=PropietarioResponse)
def update_some_propietario(propietario_id: int, propietario: PropietarioCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return update_propietario(db, propietario_id, propietario, user)

@router.delete("/{propietario_id}", response_model=PropietarioResponse)
def remove_propietario(propietario_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return delete_propietario(db, propietario_id, user)
