from sqlalchemy import or_
from app.models.renta import Renta
from app.schemas.renta import RentaCreate
from app.models.propiedad import Propiedad
from sqlalchemy.orm import Session, joinedload
import math

def get_all_rentas_without_pagination(
    db: Session, 
    q: str = None, 
    propiedad_id: int = None
):
    query = db.query(Renta)

    if q:
        query = query.filter(or_(
            Renta.nombre_comercial.ilike(f"%{q}%"),
            Renta.razon_social.ilike(f"%{q}%")
        ))

    if propiedad_id:
        query = query.join(Renta.propiedades).filter(Propiedad.id == propiedad_id)

    return query.all()

def get_all_rentas(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Renta)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    rentas = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": rentas
    }

def get_renta_by_id(db: Session, renta_id: int):
    return db.query(Renta).filter(Renta.id == renta_id).first()

def create_renta(db: Session, renta: RentaCreate):
    new_renta = Renta(**renta.dict())
    db.add(new_renta)
    db.commit()
    db.refresh(new_renta)
    return new_renta

def add_propiedad_to_renta(db: Session, renta_id: int, propiedad_id: int):
    renta = db.query(Renta).filter(Renta.id == renta_id).first()
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    renta.propiedades.append(propiedad)
    db.commit()
    db.refresh(renta)
    return renta

def remove_propiedad_from_renta(db: Session, renta_id: int, propiedad_id: int):
    renta = db.query(Renta).filter(Renta.id == renta_id).first()
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    renta.propiedades.remove(propiedad)
    db.commit()
    db.refresh(renta)
    return renta

def update_renta(db: Session, renta_id: int, renta: RentaCreate):
    db.query(Renta).filter(Renta.id == renta_id).update(renta.dict())
    db.commit()
    return db.query(Renta).filter(Renta.id == renta_id).first()

def delete_renta(db: Session, renta_id: int):
    renta = db.query(Renta).filter(Renta.id == renta_id).first()
    if renta:
        db.delete(renta)
        db.commit()
    return renta