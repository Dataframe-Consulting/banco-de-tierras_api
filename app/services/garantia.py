import math
from app.models.garantia import Garantia
from sqlalchemy.orm import Session, joinedload
from app.schemas.garantia import GarantiaCreate

def get_all_garantias_without_pagination(
    db: Session,
    q: str = None,
    propiedad_id: int = None
):
    query = db.query(Garantia)

    if(q):
        query = query.filter(Garantia.beneficiario.ilike(f"%{q}%"))

    if(propiedad_id):
        query = query.filter(Garantia.propiedad_id == propiedad_id)

    return query.all()

def get_all_garantias(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Garantia)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    garantias = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": garantias
    }

def get_garantia_by_id(db: Session, garantia_id: int):
    return db.query(Garantia).filter(Garantia.id == garantia_id).first()

def create_garantia(db: Session, garantia: GarantiaCreate):
    new_garantia = Garantia(**garantia.dict())
    db.add(new_garantia)
    db.commit()
    db.refresh(new_garantia)
    return new_garantia

def update_garantia(db: Session, garantia_id: int, garantia: GarantiaCreate):
    db.query(Garantia).filter(Garantia.id == garantia_id).update(garantia.dict())
    db.commit()
    return db.query(Garantia).filter(Garantia.id == garantia_id).first()

def delete_garantia(db: Session, garantia_id: int):
    garantia = db.query(Garantia).options(
        joinedload(Garantia.propiedad)
    ).filter(Garantia.id == garantia_id).first()
    if garantia:
        db.delete(garantia)
        db.commit()
    return garantia