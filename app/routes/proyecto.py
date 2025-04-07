from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.proyecto import ProyectoCreate, ProyectoResponse
from app.services.proyecto import get_all_proyectos_without_pagination, get_proyecto_by_id, get_proyecto_by_nombre, create_proyecto, add_propietario_to_proyecto, remove_propietario_from_proyecto, update_proyecto, delete_proyecto
from app.services.situacion_fisica import get_situacion_fisica_by_id
from app.services.vocacion import get_vocacion_by_id
from app.services.vocacion_especifica import get_vocacion_especifica_by_id
from app.services.propietario import get_propietario_by_id

router = APIRouter(prefix="/proyecto", tags=["Proyectos"])

# @router.get("/", response_model=PaginatedProyectosResponse)
# def get_proyectos(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_proyectos(db, page, page_size)

@router.get("/", response_model=List[ProyectoResponse])
def get_proyectos(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Busca por nombre..."),
    propietario_id: Optional[int] = Query(None, description="Filtrar por ID de propietario"),
    situacion_fisica_id: Optional[int] = Query(None, description="Filtrar por ID de situación física"),
    vocacion_id: Optional[int] = Query(None, description="Filtrar por ID de vocación"),
    vocacion_especifica_id: Optional[int] = Query(None, description="Filtrar por ID de vocación específica")
):
    return get_all_proyectos_without_pagination(db, q, propietario_id, situacion_fisica_id, vocacion_id, vocacion_especifica_id)

@router.get("/{proyecto_id}", response_model=ProyectoResponse)
def get_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_proyecto = get_proyecto_by_id(db, proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_proyecto

@router.post("/", response_model=ProyectoResponse)
def create_new_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_proyecto = get_proyecto_by_nombre(db, proyecto.nombre)
    if db_proyecto:
        raise HTTPException(status_code=400, detail="El proyecto ya está registrado")
    db_situacion_fisica = get_situacion_fisica_by_id(db, proyecto.situacion_fisica_id)
    if not db_situacion_fisica:
        raise HTTPException(status_code=404, detail="Situación física no encontrada")
    db_vocacion = get_vocacion_by_id(db, proyecto.vocacion_id)
    if not db_vocacion:
        raise HTTPException(status_code=404, detail="Vocación no encontrada")
    db_vocacion_especifica = get_vocacion_especifica_by_id(db, proyecto.vocacion_especifica_id)
    if not db_vocacion_especifica:
        raise HTTPException(status_code=404, detail="Vocación específica no encontrada")
    return create_proyecto(db, proyecto, user)

@router.post("/{proyecto_id}/propietario/{propietario_id}", response_model=ProyectoResponse)
def add_propietario_to_some_proyecto(proyecto_id: int, propietario_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_proyecto = get_proyecto_by_id(db, proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    propietario_already_added = any(db_propietario.id == propietario.id for propietario in db_proyecto.propietarios)
    if propietario_already_added:
        raise HTTPException(status_code=400, detail="Propietario ya agregado al proyecto")
    return add_propietario_to_proyecto(db, proyecto_id, propietario_id, user)

@router.delete("/{proyecto_id}/propietario/{propietario_id}", response_model=ProyectoResponse)
def remove_propietario_from_some_proyecto(proyecto_id: int, propietario_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_proyecto = get_proyecto_by_id(db, proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    propietario_not_added = all(db_propietario.id != propietario.id for propietario in db_proyecto.propietarios)
    if propietario_not_added:
        raise HTTPException(status_code=400, detail="Propietario no agregado al proyecto")
    return remove_propietario_from_proyecto(db, proyecto_id, propietario_id, user)

@router.put("/{proyecto_id}", response_model=ProyectoResponse)
def update_some_proyecto(proyecto_id: int, proyecto: ProyectoCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_proyecto = get_proyecto_by_id(db, proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db_situacion_fisica = get_situacion_fisica_by_id(db, proyecto.situacion_fisica_id)
    if not db_situacion_fisica:
        raise HTTPException(status_code=404, detail="Situación física no encontrada")
    db_vocacion = get_vocacion_by_id(db, proyecto.vocacion_id)
    if not db_vocacion:
        raise HTTPException(status_code=404, detail="Vocación no encontrada")
    db_vocacion_especifica = get_vocacion_especifica_by_id(db, proyecto.vocacion_especifica_id)
    if not db_vocacion_especifica:
        raise HTTPException(status_code=404, detail="Vocación específica no encontrada")
    return update_proyecto(db, proyecto_id, proyecto, user)

@router.delete("/{proyecto_id}", response_model=ProyectoResponse)
def remove_proyecto(proyecto_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_proyecto = get_proyecto_by_id(db, proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return delete_proyecto(db, proyecto_id, user)