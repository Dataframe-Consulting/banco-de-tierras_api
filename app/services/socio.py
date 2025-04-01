from sqlalchemy.orm import Session
from app.models.socio import Socio
from app.schemas.socio import SocioCreate
import math
from app.models.user import User
from app.services.auditoria import create_auditoria

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

def create_socio(db: Session, socio: SocioCreate, user: User = None):
    new_socio = Socio(**socio.dict())
    db.add(new_socio)
    db.commit()
    db.refresh(new_socio)

    valores_nuevos = {column.name: getattr(new_socio, column.name) for column in new_socio.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "socio",
        new_socio.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_socio

def update_socio(db: Session, socio_id: int, socio: SocioCreate, user: User = None):
    # db.query(Socio).filter(Socio.id == socio_id).update(socio.dict())
    # db.commit()
    # return db.query(Socio).filter(Socio.id == socio_id).first()
    existing_socio = db.query(Socio).filter(Socio.id == socio_id).first()
    valores_anteriores = {column.name: getattr(existing_socio, column.name) for column in existing_socio.__table__.columns}

    db.query(Socio).filter(Socio.id == socio_id).update(socio.dict())
    db.commit()
    updated_socio = db.query(Socio).filter(Socio.id == socio_id).first()

    valores_nuevos = {column.name: getattr(updated_socio, column.name) for column in updated_socio.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "socio",
        updated_socio.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )
    
    return updated_socio

def delete_socio(db: Session, socio_id: int, user: User = None):
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    if socio:
        valores_anteriores = {column.name: getattr(socio, column.name) for column in socio.__table__.columns}
        db.delete(socio)
        db.commit()
        create_auditoria(
            db,
            "ELIMINAR",
            "socio",
            socio_id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
    return socio