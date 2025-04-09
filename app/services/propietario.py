import math
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.auditoria import create_auditoria

from app.models.propietario import Propietario
from app.schemas.propietario import PropietarioCreate

def get_all_propietarios_without_pagination(db: Session):
    return db.query(Propietario).all()

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

def create_propietario(db: Session, propietario: PropietarioCreate, user: User = None):
    new_propietario = Propietario(**propietario.dict())
    db.add(new_propietario)
    db.commit()
    db.refresh(new_propietario)

    valores_nuevos = {column.name: getattr(new_propietario, column.name) for column in new_propietario.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "propietario",
        new_propietario.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_propietario

def update_propietario(db: Session, propietario_id: int, propietario: PropietarioCreate, user: User = None):
    existing_propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    valores_anteriores = {column.name: getattr(existing_propietario, column.name) for column in existing_propietario.__table__.columns}

    db.query(Propietario).filter(Propietario.id == propietario_id).update(propietario.dict())
    db.commit()
    updated_propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()

    valores_nuevos = {column.name: getattr(updated_propietario, column.name) for column in updated_propietario.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "propietario",
        updated_propietario.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_propietario

def delete_propietario(db: Session, propietario_id: int, user: User = None):
    propietario = db.query(Propietario).filter(Propietario.id == propietario_id).first()
    if propietario:
        valores_anteriores = {column.name: getattr(propietario, column.name) for column in propietario.__table__.columns}
        db.delete(propietario)
        db.commit()

        create_auditoria(
            db,
            "ELIMINAR",
            "propietario",
            propietario.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )

    return propietario
