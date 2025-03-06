from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ubicacion import UbicacionCreate, UbicacionResponse, PaginatedUbicacionesResponse
from app.services.ubicacion import get_all_ubicaciones, get_all_ubicaciones_without_pagination, get_ubicacion_by_id, get_ubicacion_by_nombre, create_ubicacion, update_ubicacion, delete_ubicacion

router = APIRouter(prefix="/ubicacion", tags=["Ubicaciones"])

# @router.get("/", response_model=PaginatedUbicacionesResponse)
# def get_ubicaciones(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_ubicaciones(db, page, page_size)

@router.get("/", response_model=List[UbicacionResponse])
def get_ubicaciones(db: Session = Depends(get_db)):
    return get_all_ubicaciones_without_pagination(db)

@router.get("/{ubicacion_id}", response_model=UbicacionResponse)
def get_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    db_ubicacion = get_ubicacion_by_id(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return db_ubicacion

@router.post("/", response_model=UbicacionResponse)
def create_new_ubicacion(ubicacion: UbicacionCreate, db: Session = Depends(get_db)):
    db_ubicacion = get_ubicacion_by_nombre(db, ubicacion.nombre)
    if db_ubicacion:
        raise HTTPException(status_code=400, detail="La ubicación ya está registrada")
    return create_ubicacion(db, ubicacion)

@router.put("/{ubicacion_id}", response_model=UbicacionResponse)
def update_some_ubicacion(ubicacion_id: int, ubicacion: UbicacionCreate, db: Session = Depends(get_db)):
    db_ubicacion = get_ubicacion_by_id(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return update_ubicacion(db, ubicacion_id, ubicacion)

@router.delete("/{ubicacion_id}", response_model=UbicacionResponse)
def delete_some_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    db_ubicacion = get_ubicacion_by_id(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return delete_ubicacion(db, ubicacion_id)