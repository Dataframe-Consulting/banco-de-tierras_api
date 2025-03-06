from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.propiedad import PropiedadCreate, PropiedadResponse, PaginatedPropiedadesResponse
from app.services.propiedad import get_all_propiedades, get_all_propiedades_without_pagination, get_propiedad_by_id, get_propiedad_by_nombre, get_propiedad_by_clave_catastral, create_propiedad, add_ubicacion_to_propiedad, remove_ubicacion_from_propiedad, update_propiedad, delete_propiedad
from app.services.proyecto import get_proyecto_by_id
from app.services.ubicacion import get_ubicacion_by_id
from app.utils.auth import get_current_user

router = APIRouter(prefix="/propiedad", tags=["Propiedades"])

# @router.get("/", response_model=PaginatedPropiedadesResponse)
# def get_propiedades(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_propiedades(db, page, page_size)

@router.get("/", response_model=List[PropiedadResponse])
def get_propiedades(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Busca por nombre..."),
    proyecto_id: Optional[int] = Query(None, description="Filtrar por ID de proyecto"),
    ubicacion_id: Optional[int] = Query(None, description="Filtrar por ID de ubicación")
):
    return get_all_propiedades_without_pagination(db, q, proyecto_id, ubicacion_id)

@router.get("/{propiedad_id}", response_model=PropiedadResponse)
def get_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return db_propiedad

@router.post("/", response_model=PropiedadResponse)
def create_new_propiedad(propiedad: PropiedadCreate, db: Session = Depends(get_db)):
    db_propiedad_nombre = get_propiedad_by_nombre(db, propiedad.nombre)
    if db_propiedad_nombre:
        raise HTTPException(status_code=400, detail="La propiedad con este nombre ya está registrada")
    db_propiedad_clave = get_propiedad_by_clave_catastral(db, propiedad.clave_catastral)
    if db_propiedad_clave:
        raise HTTPException(status_code=400, detail="La propiedad con esta clave catastral ya está registrada")
    db_proyecto = get_proyecto_by_id(db, propiedad.proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return create_propiedad(db, propiedad)

@router.post("/{propiedad_id}/ubicacion/{ubicacion_id}", response_model=PropiedadResponse)
def add_ubicacion_to_some_propiedad(propiedad_id: int, ubicacion_id: int, db: Session = Depends(get_db)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_ubicacion = get_ubicacion_by_id(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    ubicacion_already_added = any(db_ubicacion.id == ubicacion.id for ubicacion in db_propiedad.ubicaciones)
    if ubicacion_already_added:
        raise HTTPException(status_code=400, detail="Ubicación ya agregada a la propiedad")
    return add_ubicacion_to_propiedad(db, propiedad_id, ubicacion_id)

@router.delete("/{propiedad_id}/ubicacion/{ubicacion_id}", response_model=PropiedadResponse)
def remove_ubicacion_from_some_propiedad(propiedad_id: int, ubicacion_id: int, db: Session = Depends(get_db)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_ubicacion = get_ubicacion_by_id(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    ubicacion_not_added = all(db_ubicacion.id != ubicacion.id for ubicacion in db_propiedad.ubicaciones)
    if ubicacion_not_added:
        raise HTTPException(status_code=400, detail="Ubicación no agregada a la propiedad")
    return remove_ubicacion_from_propiedad(db, propiedad_id, ubicacion_id)

@router.put("/{propiedad_id}", response_model=PropiedadResponse)
def update_existing_propiedad(propiedad_id: int, propiedad: PropiedadCreate, db: Session = Depends(get_db)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_proyecto = get_proyecto_by_id(db, propiedad.proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return update_propiedad(db, propiedad_id, propiedad)

@router.delete("/{propiedad_id}", response_model=PropiedadResponse)
def delete_existing_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return delete_propiedad(db, propiedad_id)