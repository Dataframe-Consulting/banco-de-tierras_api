from sqlalchemy.orm import Session, joinedload
from app.models.ubicacion import Ubicacion
from app.schemas.ubicacion import UbicacionCreate
import math

def get_all_ubicaciones_without_pagination(db: Session):
    return db.query(Ubicacion).all()

def get_all_ubicaciones(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Ubicacion)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    ubicaciones = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": ubicaciones
    }

def get_ubicacion_by_id(db: Session, ubicacion_id: int):
    return db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()

def get_ubicacion_by_nombre(db: Session, nombre: str):
    return db.query(Ubicacion).filter(Ubicacion.nombre == nombre).first()

def create_ubicacion(db: Session, ubicacion: UbicacionCreate):
    new_ubicacion = Ubicacion(**ubicacion.dict())
    db.add(new_ubicacion)
    db.commit()
    db.refresh(new_ubicacion)
    return new_ubicacion

def update_ubicacion(db: Session, ubicacion_id: int, ubicacion: UbicacionCreate):
    db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).update(ubicacion.dict())
    db.commit()
    return db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()

def delete_ubicacion(db: Session, ubicacion_id: int):
    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    db.delete(ubicacion)
    db.commit()
    return ubicacion