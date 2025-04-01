from sqlalchemy.orm import Session
from app.models.situacion_fisica import SituacionFisica
from app.schemas.situacion_fisica import SituacionFisicaCreate
import math

from app.models.user import User
from app.services.auditoria import create_auditoria

def get_all_situaciones_fisicas_without_pagination(db: Session):
    return db.query(SituacionFisica).all()

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

def create_situacion_fisica(db: Session, situacion_fisica: SituacionFisicaCreate, user: User = None):
    new_situacion_fisica = SituacionFisica(**situacion_fisica.dict())
    db.add(new_situacion_fisica)
    db.commit()
    db.refresh(new_situacion_fisica)

    valores_nuevos = {column.name: getattr(new_situacion_fisica, column.name) for column in new_situacion_fisica.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "situacion_fisica",
        new_situacion_fisica.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_situacion_fisica

def update_situacion_fisica(db: Session, situacion_fisica_id: int, situacion_fisica: SituacionFisicaCreate, user: User = None):
    existing_situacion_fisica = db.query(SituacionFisica).filter(SituacionFisica.id == situacion_fisica_id).first()
    valores_anteriores = {column.name: getattr(existing_situacion_fisica, column.name) for column in existing_situacion_fisica.__table__.columns}

    db.query(SituacionFisica).filter(SituacionFisica.id == situacion_fisica_id).update(situacion_fisica.dict())
    db.commit()
    updated_situacion_fisica = db.query(SituacionFisica).filter(SituacionFisica.id == situacion_fisica_id).first()

    valores_nuevos = {column.name: getattr(updated_situacion_fisica, column.name) for column in updated_situacion_fisica.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "situacion_fisica",
        updated_situacion_fisica.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_situacion_fisica

def delete_situacion_fisica(db: Session, situacion_fisica_id: int, user: User = None):
    situacion_fisica = db.query(SituacionFisica).filter(SituacionFisica.id == situacion_fisica_id).first()
    if situacion_fisica:
        valores_anteriores = {column.name: getattr(situacion_fisica, column.name) for column in situacion_fisica.__table__.columns}
        db.delete(situacion_fisica)
        db.commit()

        create_auditoria(
            db,
            "ELIMINAR",
            "situacion_fisica",
            situacion_fisica.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
    return situacion_fisica