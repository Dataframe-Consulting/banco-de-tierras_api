from sqlalchemy.orm import Session
from app.models.vocacion import Vocacion
from app.schemas.vocacion import VocacionCreate
import math

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

def create_vocacion(db: Session, vocacion: VocacionCreate):
    new_vocacion = Vocacion(**vocacion.dict())
    db.add(new_vocacion)
    db.commit()
    db.refresh(new_vocacion)
    return new_vocacion

def update_vocacion(db: Session, vocacion_id: int, vocacion: VocacionCreate):
    db.query(Vocacion).filter(Vocacion.id == vocacion_id).update(vocacion.dict())
    db.commit()
    return db.query(Vocacion).filter(Vocacion.id == vocacion_id).first()

def delete_vocacion(db: Session, vocacion_id: int):
    vocacion = db.query(Vocacion).filter(Vocacion.id == vocacion_id).first()
    if vocacion:
        db.delete(vocacion)
        db.commit()
    return vocacion