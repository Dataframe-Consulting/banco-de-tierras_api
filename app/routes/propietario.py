from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.propietario import PropietarioCreate, PropietarioResponse, PaginatedPropietariosResponse
from app.services.propietario import get_all_propietarios, get_all_propietarios_without_pagination, get_propietario_by_id, get_propietario_by_rfc, create_propietario, add_socio_to_propietario, update_propietario, delete_propietario, remove_socio_from_propietario
from app.services.socio import get_socio_by_id

router = APIRouter(prefix="/propietario", tags=["Propietarios"])

# WITH PAGINATION
# @router.get("/", response_model=PaginatedPropietariosResponse)
# def get_propietarios(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_propietarios(db, page, page_size)

# WITHOUT PAGINATION
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
def create_new_propietario(propietario: PropietarioCreate, db: Session = Depends(get_db)):
    db_propietario = get_propietario_by_rfc(db, propietario.rfc)
    if db_propietario:
        raise HTTPException(status_code=400, detail="El RFC ya está registrado")
    return create_propietario(db, propietario)

@router.post("/{propietario_id}/socio/{socio_id}", response_model=PropietarioResponse)
def add_socio_to_some_propietario(propietario_id: int, socio_id: int, db: Session = Depends(get_db)):
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    db_socio = get_socio_by_id(db, socio_id)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    socio_already_added = any(db_socio.id == socio.id for socio in db_propietario.socios)
    if socio_already_added:
        raise HTTPException(status_code=400, detail="Socio ya agregado al propietario")
    return add_socio_to_propietario(db, propietario_id, socio_id)

@router.put("/{propietario_id}", response_model=PropietarioResponse)
def update_some_propietario(propietario_id: int, propietario: PropietarioCreate, db: Session = Depends(get_db)):
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return update_propietario(db, propietario_id, propietario)

@router.delete("/{propietario_id}", response_model=PropietarioResponse)
def remove_propietario(propietario_id: int, db: Session = Depends(get_db)):
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return delete_propietario(db, propietario_id)

@router.delete("/{propietario_id}/socio/{socio_id}", response_model=PropietarioResponse)
def remove_socio_from_some_propietario(propietario_id: int, socio_id: int, db: Session = Depends(get_db)):
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    db_socio = get_socio_by_id(db, socio_id)
    if not db_socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    socio_not_added = all(db_socio.id != socio.id for socio in db_propietario.socios)
    if socio_not_added:
        raise HTTPException(status_code=400, detail="Socio no agregado al propietario")
    return remove_socio_from_propietario(db, propietario_id, socio_id)
