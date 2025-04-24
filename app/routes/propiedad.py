from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.propiedad import PropiedadCreate, PropiedadResponse
from app.services.propiedad import get_all_propiedades_without_pagination, get_propiedad_by_id, get_propiedad_by_nombre, get_propiedad_by_clave_catastral, create_propiedad, check_propietario_in_propiedad, add_propietario_to_propiedad, remove_propietario_from_propiedad, add_ubicacion_to_propiedad, remove_ubicacion_from_propiedad, add_garantia_to_propiedad, remove_garantia_from_propiedad, add_proceso_legal_to_propiedad, remove_proceso_legal_from_propiedad, update_propiedad, delete_propiedad
from app.services.proyecto import get_proyecto_by_id
from app.services.propietario import get_propietario_by_id
from app.services.garantia import get_garantia_by_id
from app.services.ubicacion import get_ubicacion_by_id
from app.services.proceso_legal import get_proceso_legal_by_id

router = APIRouter(prefix="/propiedad", tags=["Propiedades"])

@router.get("/", response_model=List[PropiedadResponse])
def get_propiedades(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Busca por nombre..."),
    proyecto_id: Optional[int] = Query(None, description="Filtrar por ID de proyecto"),
    ubicacion_id: Optional[int] = Query(None, description="Filtrar por ID de ubicación"),
    garantia_id: Optional[int] = Query(None, description="Filtrar por ID de garantía"),
    proceso_legal_id: Optional[int] = Query(None, description="Filtrar por ID de proceso legal")
):
    return get_all_propiedades_without_pagination(db, q, proyecto_id, ubicacion_id, garantia_id, proceso_legal_id)

@router.get("/{propiedad_id}", response_model=PropiedadResponse)
def get_propiedad(propiedad_id: int, db: Session = Depends(get_db)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return db_propiedad

@router.post("/", response_model=PropiedadResponse)
def create_new_propiedad(propiedad: PropiedadCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad_nombre = get_propiedad_by_nombre(db, propiedad.nombre)
    if db_propiedad_nombre:
        raise HTTPException(status_code=400, detail="La propiedad con este nombre ya está registrada")
    db_propiedad_clave = get_propiedad_by_clave_catastral(db, propiedad.clave_catastral)
    if db_propiedad_clave:
        raise HTTPException(status_code=400, detail="La propiedad con esta clave catastral ya está registrada")
    db_proyecto = get_proyecto_by_id(db, propiedad.proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return create_propiedad(db, propiedad, user)

@router.post("/{propiedad_id}/propietario/{propietario_id}/sociedad/{sociedad_porcentaje_participacion}/es_socio/{es_socio}", response_model=PropiedadResponse)
def add_propietario_sociedad_to_some_propiedad(propiedad_id: int, propietario_id: int, sociedad_porcentaje_participacion: float, es_socio: bool, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    register_already_exists = check_propietario_in_propiedad(db, propiedad_id, propietario_id)
    if register_already_exists:
        raise HTTPException(status_code=400, detail="Este registro ya existe")
    if sociedad_porcentaje_participacion <= 0 or sociedad_porcentaje_participacion > 100:
        raise HTTPException(status_code=400, detail="El porcentaje de participación debe ser mayor a 0 y menor o igual a 100")
    return add_propietario_to_propiedad(db, propiedad_id, propietario_id, sociedad_porcentaje_participacion, es_socio, user)

@router.delete("/{propiedad_id}/propietario/{propietario_id}", response_model=PropiedadResponse)
def remove_propietario_sociedad_from_some_propiedad(propiedad_id: int, propietario_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_propietario = get_propietario_by_id(db, propietario_id)
    if not db_propietario:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    register_not_exists = check_propietario_in_propiedad(db, propiedad_id, propietario_id)
    if not register_not_exists:
        raise HTTPException(status_code=400, detail="Este registro no existe")
    return remove_propietario_from_propiedad(db, propiedad_id, propietario_id, user)

@router.post("/{propiedad_id}/ubicacion/{ubicacion_id}", response_model=PropiedadResponse)
def add_ubicacion_to_some_propiedad(propiedad_id: int, ubicacion_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_ubicacion = get_ubicacion_by_id(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    ubicacion_already_added = any(db_ubicacion.id == ubicacion.id for ubicacion in db_propiedad.ubicaciones)
    if ubicacion_already_added:
        raise HTTPException(status_code=400, detail="Ubicación ya agregada a la propiedad")
    return add_ubicacion_to_propiedad(db, propiedad_id, ubicacion_id, user)

@router.delete("/{propiedad_id}/ubicacion/{ubicacion_id}", response_model=PropiedadResponse)
def remove_ubicacion_from_some_propiedad(propiedad_id: int, ubicacion_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_ubicacion = get_ubicacion_by_id(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    ubicacion_not_added = all(db_ubicacion.id != ubicacion.id for ubicacion in db_propiedad.ubicaciones)
    if ubicacion_not_added:
        raise HTTPException(status_code=400, detail="Ubicación no agregada a la propiedad")
    return remove_ubicacion_from_propiedad(db, propiedad_id, ubicacion_id, user)

@router.post("/{propiedad_id}/garantia/{garantia_id}", response_model=PropiedadResponse)
def add_garantia_to_some_propiedad(propiedad_id: int, garantia_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_garantia = get_garantia_by_id(db, garantia_id)
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantía no encontrada")
    garantia_already_added = any(db_garantia.id == garantia.id for garantia in db_propiedad.garantias)
    if garantia_already_added:
        raise HTTPException(status_code=400, detail="Garantía ya agregada a la propiedad")
    return add_garantia_to_propiedad(db, propiedad_id, garantia_id, user)

@router.delete("/{propiedad_id}/garantia/{garantia_id}", response_model=PropiedadResponse)
def remove_garantia_from_some_propiedad(propiedad_id: int, garantia_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_garantia = get_garantia_by_id(db, garantia_id)
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantía no encontrada")
    garantia_not_added = all(db_garantia.id != garantia.id for garantia in db_propiedad.garantias)
    if garantia_not_added:
        raise HTTPException(status_code=400, detail="Garantía no agregada a la propiedad")
    return remove_garantia_from_propiedad(db, propiedad_id, garantia_id, user)

@router.post("/{propiedad_id}/proceso_legal/{proceso_legal_id}", response_model=PropiedadResponse)
def add_proceso_legal_to_some_propiedad(propiedad_id: int, proceso_legal_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_proceso_legal = get_proceso_legal_by_id(db, proceso_legal_id)
    if not db_proceso_legal:
        raise HTTPException(status_code=404, detail="Proceso legal no encontrado")
    proceso_legal_already_added = any(db_proceso_legal.id == proceso_legal.id for proceso_legal in db_propiedad.procesos_legales)
    if proceso_legal_already_added:
        raise HTTPException(status_code=400, detail="Proceso legal ya agregado a la propiedad")
    return add_proceso_legal_to_propiedad(db, propiedad_id, proceso_legal_id, user)

@router.delete("/{propiedad_id}/proceso_legal/{proceso_legal_id}", response_model=PropiedadResponse)
def remove_proceso_legal_from_some_propiedad(propiedad_id: int, proceso_legal_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_proceso_legal = get_proceso_legal_by_id(db, proceso_legal_id)
    if not db_proceso_legal:
        raise HTTPException(status_code=404, detail="Proceso legal no encontrado")
    proceso_legal_not_added = all(db_proceso_legal.id != proceso_legal.id for proceso_legal in db_propiedad.procesos_legales)
    if proceso_legal_not_added:
        raise HTTPException(status_code=400, detail="Proceso legal no agregado a la propiedad")
    return remove_proceso_legal_from_propiedad(db, propiedad_id, proceso_legal_id, user)

@router.put("/{propiedad_id}", response_model=PropiedadResponse)
def update_existing_propiedad(propiedad_id: int, propiedad: PropiedadCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    db_proyecto = get_proyecto_by_id(db, propiedad.proyecto_id)
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return update_propiedad(db, propiedad_id, propiedad, user)

@router.delete("/{propiedad_id}", response_model=PropiedadResponse)
def delete_existing_propiedad(propiedad_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return delete_propiedad(db, propiedad_id, user)