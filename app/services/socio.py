from sqlalchemy.orm import Session
from app.models.socio import Socio
from app.schemas.socio import SocioCreate
import math

def get_all_socios_without_pagination(db: Session):
    return db.query(Socio).all()

def get_all_socios(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Socio)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    socios = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": socios
    }

def get_socio_by_id(db: Session, socio_id: int):
    return db.query(Socio).filter(Socio.id == socio_id).first()

def create_socio(db: Session, socio: SocioCreate):
    new_socio = Socio(**socio.dict())
    db.add(new_socio)
    db.commit()
    db.refresh(new_socio)
    return new_socio

def update_socio(db: Session, socio_id: int, socio: SocioCreate):
    db.query(Socio).filter(Socio.id == socio_id).update(socio.dict())
    db.commit()
    return db.query(Socio).filter(Socio.id == socio_id).first()

def delete_socio(db: Session, socio_id: int):
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    if socio:
        db.delete(socio)
        db.commit()
    return socio