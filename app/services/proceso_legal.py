import math
from sqlalchemy.orm import Session

from app.models.user import User

from app.models.proceso_legal import ProcesoLegal
from app.schemas.proceso_legal import ProcesoLegalCreate
from app.services.auditoria import create_auditoria

def get_all_procesos_legales_without_pagination(
    db: Session,
    q: str = None,
):
    query = db.query(ProcesoLegal)

    if(q):
        query = query.filter(ProcesoLegal.abogado.ilike(f"%{q}%"))

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

def create_proceso_legal(db: Session, proceso_legal: ProcesoLegalCreate, user: User = None):
    new_proceso_legal = ProcesoLegal(**proceso_legal.dict())
    db.add(new_proceso_legal)
    db.commit()
    db.refresh(new_proceso_legal)
    
    valores_nuevos = {column.name: getattr(new_proceso_legal, column.name) for column in new_proceso_legal.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "proceso_legal",
        new_proceso_legal.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )
    return new_proceso_legal

def update_proceso_legal(db: Session, proceso_legal_id: int, proceso_legal: ProcesoLegalCreate, user: User = None):
    existing_proceso_legal = db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).first()
    valores_anteriores = {column.name: getattr(existing_proceso_legal, column.name) for column in existing_proceso_legal.__table__.columns}

    db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).update(proceso_legal.dict())
    db.commit()
    updated_proceso_legal = db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).first()

    valores_nuevos = {column.name: getattr(updated_proceso_legal, column.name) for column in updated_proceso_legal.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "proceso_legal",
        updated_proceso_legal.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_proceso_legal

def delete_proceso_legal(db: Session, proceso_legal_id: int, user: User = None):
    proceso_legal = db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).first()
    if proceso_legal:
        valores_anteriores = {column.name: getattr(proceso_legal, column.name) for column in proceso_legal.__table__.columns}

        db.delete(proceso_legal)
        db.commit()

        create_auditoria(
            db,
            "ELIMINAR",
            "proceso_legal",
            proceso_legal.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
    return proceso_legal