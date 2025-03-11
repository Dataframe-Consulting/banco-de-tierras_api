from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from app.models.proyecto import Proyecto, SociedadProyecto
from app.schemas.proyecto import ProyectoCreate
from app.models.propietario import Propietario
from app.models.sociedad import Sociedad
import math

def get_all_proyectos_without_pagination(
    db: Session,
    q: str = None,
    propietario_id: int = None,
    situacion_fisica_id: int = None,
    sociedad_id: int = None,
    vocacion_id: int = None,
    vocacion_especifica_id: int = None
):
    query = db.query(Proyecto)

    if(q):
        query = query.filter(Proyecto.nombre.ilike(f"%{q}%"))

    if(propietario_id):
        query = query.join(Proyecto.propietarios).filter(Propietario.id == propietario_id)

    if(situacion_fisica_id):
        query = query.filter(Proyecto.situacion_fisica_id == situacion_fisica_id)

    if(sociedad_id):
        query = query.filter(Proyecto.sociedades.any(SociedadProyecto.sociedad_id == sociedad_id))

    if(vocacion_id):
        query = query.filter(Proyecto.vocacion_id == vocacion_id)

    if(vocacion_especifica_id):
        query = query.filter(Proyecto.vocacion_especifica_id == vocacion_especifica_id)

    return query.all()

def get_all_proyectos(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Proyecto)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    proyectos = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": proyectos
    }

def get_proyecto_by_id(db: Session, proyecto_id: int):
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()

def get_proyecto_by_nombre(db: Session, nombre: str):
    return db.query(Proyecto).filter(Proyecto.nombre == nombre).first()

def create_proyecto(db: Session, proyecto: ProyectoCreate):
    new_proyecto = Proyecto(**proyecto.dict())
    db.add(new_proyecto)
    db.commit()
    db.refresh(new_proyecto)
    return new_proyecto

def add_propietario_to_proyecto(db: Session, proyecto_id: int, propietario_id: int):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    proyecto.propietarios.append(propietario)
    db.commit()
    db.refresh(proyecto)
    return proyecto

def remove_propietario_from_proyecto(db: Session, proyecto_id: int, propietario_id: int):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    proyecto.propietarios.remove(propietario)
    db.commit()
    db.refresh(proyecto)
    return proyecto

def add_sociedad_to_proyecto(db: Session, proyecto_id: int, sociedad_id: int, valor: float):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    sociedad = db.query(Sociedad).filter(Sociedad.id == sociedad_id).first()
    sociedad_proyecto = SociedadProyecto(valor=valor, proyecto_id=proyecto_id, sociedad_id=sociedad_id)
    db.add(sociedad_proyecto)
    proyecto.sociedades.append(sociedad_proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto

def check_sociedad_in_proyecto(db: Session, proyecto_id: int, sociedad_id: int):
    return db.query(SociedadProyecto).filter(SociedadProyecto.proyecto_id == proyecto_id, SociedadProyecto.sociedad_id == sociedad_id).first()

def remove_sociedad_from_proyecto(db: Session, proyecto_id: int, sociedad_id: int):
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    sociedad_proyecto = db.query(SociedadProyecto).filter(SociedadProyecto.proyecto_id == proyecto_id, SociedadProyecto.sociedad_id == sociedad_id).first()
    db.delete(sociedad_proyecto)
    db.commit()
    db.refresh(proyecto)
    return proyecto

def update_proyecto(db: Session, proyecto_id: int, proyecto: ProyectoCreate):
    db.query(Proyecto).filter(Proyecto.id == proyecto_id).update(proyecto.dict())
    db.commit()
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()

def delete_proyecto(db: Session, proyecto_id: int):
    db.query(SociedadProyecto).filter(SociedadProyecto.proyecto_id == proyecto_id).delete()
    db.commit()

    proyecto = db.query(Proyecto).options(
        joinedload(Proyecto.situacion_fisica),
        joinedload(Proyecto.vocacion),
        joinedload(Proyecto.vocacion_especifica)
    ).filter(Proyecto.id == proyecto_id).first()
    if proyecto:
        db.delete(proyecto)
        db.commit()
    return proyecto
