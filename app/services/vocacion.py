from sqlalchemy.orm import Session
from app.models.vocacion import Vocacion
from app.schemas.vocacion import VocacionCreate
import math
from app.models.user import User
from app.services.auditoria import create_auditoria

def get_all_vocaciones_without_pagination(db: Session):
    return db.query(Vocacion).all()

def get_all_vocaciones(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Vocacion)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    vocaciones = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": vocaciones
    }

def get_vocacion_by_id(db: Session, vocacion_id: int):
    return db.query(Vocacion).filter(Vocacion.id == vocacion_id).first()

def get_vocacion_by_valor(db: Session, valor: str):
    return db.query(Vocacion).filter(Vocacion.valor == valor).first()

def create_vocacion(db: Session, vocacion: VocacionCreate, user: User = None):
    new_vocacion = Vocacion(**vocacion.dict())
    db.add(new_vocacion)
    db.commit()
    db.refresh(new_vocacion)

    valores_nuevos = {column.name: getattr(new_vocacion, column.name) for column in new_vocacion.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "vocacion",
        new_vocacion.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_vocacion

def update_vocacion(db: Session, vocacion_id: int, vocacion: VocacionCreate, user: User = None):
    existing_vocacion = db.query(Vocacion).filter(Vocacion.id == vocacion_id).first()
    valores_anteriores = {column.name: getattr(existing_vocacion, column.name) for column in Vocacion.__table__.columns}

    db.query(Vocacion).filter(Vocacion.id == vocacion_id).update(vocacion.dict())
    db.commit()
    updated_vocacion = db.query(Vocacion).filter(Vocacion.id == vocacion_id).first()

    valores_nuevos = {column.name: getattr(updated_vocacion, column.name) for column in Vocacion.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "vocacion",
        updated_vocacion.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_vocacion

def delete_vocacion(db: Session, vocacion_id: int, user: User = None):
    vocacion = db.query(Vocacion).filter(Vocacion.id == vocacion_id).first()
    if vocacion:
        valores_anteriores = {column.name: getattr(vocacion, column.name) for column in Vocacion.__table__.columns}
        db.delete(vocacion)
        db.commit()

        create_auditoria(
            db,
            "ELIMINAR",
            "vocacion",
            vocacion.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
    return vocacion