from sqlalchemy.orm import Session, joinedload
from app.models.ubicacion import Ubicacion
from app.schemas.ubicacion import UbicacionCreate
import math
from app.models.user import User
from app.services.auditoria import create_auditoria

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

def create_ubicacion(db: Session, ubicacion: UbicacionCreate, user: User = None):
    new_ubicacion = Ubicacion(**ubicacion.dict())
    db.add(new_ubicacion)
    db.commit()
    db.refresh(new_ubicacion)

    valores_nuevos = {column.name: getattr(new_ubicacion, column.name) for column in new_ubicacion.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "ubicacion",
        new_ubicacion.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_ubicacion

def update_ubicacion(db: Session, ubicacion_id: int, ubicacion: UbicacionCreate, user: User = None):
    existing_ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    valores_anteriores = {column.name: getattr(existing_ubicacion, column.name) for column in existing_ubicacion.__table__.columns}

    db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).update(ubicacion.dict())
    db.commit()
    updated_ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()

    valores_nuevos = {column.name: getattr(updated_ubicacion, column.name) for column in updated_ubicacion.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "ubicacion",
        updated_ubicacion.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_ubicacion

def delete_ubicacion(db: Session, ubicacion_id: int, user: User = None):
    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()

    valores_anteriores = {column.name: getattr(ubicacion, column.name) for column in ubicacion.__table__.columns}

    db.delete(ubicacion)
    db.commit()

    create_auditoria(
        db,
        "ELIMINAR",
        "ubicacion",
        ubicacion.id,
        user.username if user else None,
        valores_anteriores,
        None,
    )
    return ubicacion