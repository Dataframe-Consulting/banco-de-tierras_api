from sqlalchemy.orm import Session
from app.models.propietario import Propietario
from app.models.socio import Socio
from app.schemas.propietario import PropietarioCreate
from app.schemas.socio import SocioCreate
import math

def get_all_propietarios(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Propietario)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    propietarios = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": propietarios
    }

def get_propietario_by_id(db: Session, propietario_id: int):
    return db.query(Propietario).filter(Propietario.id == propietario_id).first()

def get_propietario_by_rfc(db: Session, rfc: str):
    return db.query(Propietario).filter(Propietario.rfc == rfc).first()

def create_propietario(db: Session, propietario: PropietarioCreate):
    new_propietario = Propietario(**propietario.dict())
    db.add(new_propietario)
    db.commit()
    db.refresh(new_propietario)
    return new_propietario

def add_socio_to_propietario(db: Session, propietario_id: int, socio_id: int):
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    propietario.socios.append(socio)
    db.commit()
    db.refresh(propietario)
    return propietario

def remove_socio_from_propietario(db: Session, propietario_id: int, socio_id: int):
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    propietario.socios.remove(socio)
    db.commit()
    db.refresh(propietario)
    return propietario

def update_propietario(db: Session, propietario_id: int, propietario: PropietarioCreate):
    db.query(Propietario).filter(Propietario.id == propietario_id).update(propietario.dict())
    db.commit()
    return db.query(Propietario).filter(Propietario.id == propietario_id).first()

def delete_propietario(db: Session, propietario_id: int):
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    if propietario:
        db.delete(propietario)
        db.commit()
    return propietario
