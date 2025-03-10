from sqlalchemy.orm import Session
from app.models.sociedad import Sociedad
from app.schemas.sociedad import SociedadCreate
import math

def get_all_sociedades_without_pagination(db: Session):
    return db.query(Sociedad).all()

def get_all_sociedades(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Sociedad)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    sociedades = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": sociedades
    }

def get_sociedad_by_id(db: Session, sociedad_id: int):
    return db.query(Sociedad).filter(Sociedad.id == sociedad_id).first()

def get_sociedad_by_porcentaje(db: Session, porcentaje_participacion: float):
    return db.query(Sociedad).filter(Sociedad.porcentaje_participacion == porcentaje_participacion).first()

def create_sociedad(db: Session, sociedad: SociedadCreate):
    new_sociedad = Sociedad(**sociedad.dict())
    db.add(new_sociedad)
    db.commit()
    db.refresh(new_sociedad)
    return new_sociedad

def update_sociedad(db: Session, sociedad_id: int, sociedad: SociedadCreate):
    db.query(Sociedad).filter(Sociedad.id == sociedad_id).update(sociedad.dict())
    db.commit()
    return db.query(Sociedad).filter(Sociedad.id == sociedad_id).first()

def delete_sociedad(db: Session, sociedad_id: int):
    sociedad = db.query(Sociedad).filter(Sociedad.id == sociedad_id).first()
    if sociedad:
        db.delete(sociedad)
        db.commit()
    return sociedad