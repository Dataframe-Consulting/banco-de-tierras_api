from sqlalchemy.orm import Session
from app.models.situacion_fisica import SituacionFisica
from app.schemas.situacion_fisica import SituacionFisicaCreate
import math

def get_all_situaciones_fisicas(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(SituacionFisica)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    situaciones_fisicas = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": situaciones_fisicas
    }

def get_situacion_fisica_by_id(db: Session, situacion_fisica_id: int):
    return db.query(SituacionFisica).filter(SituacionFisica.id == situacion_fisica_id).first()

def get_situacion_fisica_by_nombre(db: Session, nombre: str):
    return db.query(SituacionFisica).filter(SituacionFisica.nombre == nombre).first()

def create_situacion_fisica(db: Session, situacion_fisica: SituacionFisicaCreate):
    new_situacion_fisica = SituacionFisica(**situacion_fisica.dict())
    db.add(new_situacion_fisica)
    db.commit()
    db.refresh(new_situacion_fisica)
    return new_situacion_fisica

def update_situacion_fisica(db: Session, situacion_fisica_id: int, situacion_fisica: SituacionFisicaCreate):
    db.query(SituacionFisica).filter(SituacionFisica.id == situacion_fisica_id).update(situacion_fisica.dict())
    db.commit()
    return db.query(SituacionFisica).filter(SituacionFisica.id == situacion_fisica_id).first()

def delete_situacion_fisica(db: Session, situacion_fisica_id: int):
    situacion_fisica = db.query(SituacionFisica).filter(SituacionFisica.id == situacion_fisica_id).first()
    if situacion_fisica:
        db.delete(situacion_fisica)
        db.commit()
    return situacion_fisica