from sqlalchemy.orm import Session
from app.models.sociedad import Sociedad
from app.schemas.sociedad import SociedadCreate
import math
from app.models.user import User
from app.services.auditoria import create_auditoria

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

def create_sociedad(db: Session, sociedad: SociedadCreate, user: User = None):
    new_sociedad = Sociedad(**sociedad.dict())
    db.add(new_sociedad)
    db.commit()
    db.refresh(new_sociedad)

    valores_nuevos = {column.name: getattr(new_sociedad, column.name) for column in new_sociedad.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "sociedad",
        new_sociedad.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_sociedad

def update_sociedad(db: Session, sociedad_id: int, sociedad: SociedadCreate, user: User = None):
    existing_sociedad = db.query(Sociedad).filter(Sociedad.id == sociedad_id).first()
    valores_anteriores = {column.name: getattr(existing_sociedad, column.name) for column in existing_sociedad.__table__.columns}

    db.query(Sociedad).filter(Sociedad.id == sociedad_id).update(sociedad.dict())
    db.commit()
    updated_sociedad = db.query(Sociedad).filter(Sociedad.id == sociedad_id).first()

    valores_nuevos = {column.name: getattr(updated_sociedad, column.name) for column in updated_sociedad.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "sociedad",
        updated_sociedad.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_sociedad

def delete_sociedad(db: Session, sociedad_id: int, user: User = None):
    sociedad = db.query(Sociedad).filter(Sociedad.id == sociedad_id).first()
    if sociedad:
        valores_anteriores = {column.name: getattr(sociedad, column.name) for column in sociedad.__table__.columns}
        db.delete(sociedad)
        db.commit()

        create_auditoria(
            db,
            "ELIMINAR",
            "sociedad",
            sociedad.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
    return sociedad