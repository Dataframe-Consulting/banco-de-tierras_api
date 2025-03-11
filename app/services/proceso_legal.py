from sqlalchemy.orm import Session, joinedload
from app.models.proceso_legal import ProcesoLegal
from app.schemas.proceso_legal import ProcesoLegalCreate
import math

def get_all_procesos_legales_without_pagination(
    db: Session,
    q: str = None,
    propiedad_id: int = None
):
    query = db.query(ProcesoLegal)

    if(q):
        query = query.filter(ProcesoLegal.abogado.ilike(f"%{q}%"))

    if(propiedad_id):
        query = query.filter(ProcesoLegal.propiedad_id == propiedad_id)

    return query.all()

def get_all_procesos_legales(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(ProcesoLegal)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    procesos_legales = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": procesos_legales
    }

def get_proceso_legal_by_id(db: Session, proceso_legal_id: int):
    return db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).first()

def create_proceso_legal(db: Session, proceso_legal: ProcesoLegalCreate):
    new_proceso_legal = ProcesoLegal(**proceso_legal.dict())
    db.add(new_proceso_legal)
    db.commit()
    db.refresh(new_proceso_legal)
    return new_proceso_legal

def update_proceso_legal(db: Session, proceso_legal_id: int, proceso_legal: ProcesoLegalCreate):
    db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).update(proceso_legal.dict())
    db.commit()
    return db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).first()

def delete_proceso_legal(db: Session, proceso_legal_id: int):
    proceso_legal = db.query(ProcesoLegal).options(
        joinedload(ProcesoLegal.propiedad)
    ).filter(ProcesoLegal.id == proceso_legal_id).first()
    if proceso_legal:
        db.delete(proceso_legal)
        db.commit()
    return proceso_legal