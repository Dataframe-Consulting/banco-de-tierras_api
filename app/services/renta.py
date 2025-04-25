from sqlalchemy import or_
from app.models.renta import Renta
from app.schemas.renta import RentaCreate
from app.models.propiedad import Propiedad
from sqlalchemy.orm import Session, joinedload
import math

from app.models.user import User
from app.services.auditoria import create_auditoria

def get_all_rentas_without_pagination(
    db: Session, 
    q: str = None, 
    propiedad_id: int = None,
    proyecto_id: int = None,
):
    query = db.query(Renta)

    if q:
        query = query.filter(or_(
            Renta.nombre_comercial.ilike(f"%{q}%"),
            Renta.razon_social.ilike(f"%{q}%")
        ))

    if propiedad_id:
        query = query.join(Renta.propiedades).filter(Propiedad.id == propiedad_id)

    if proyecto_id:
        query = query.filter(Renta.propiedades.any(Propiedad.proyecto_id == proyecto_id))

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

def create_renta(db: Session, renta: RentaCreate, user: User = None):
    new_renta = Renta(**renta.dict())
    db.add(new_renta)
    db.commit()
    db.refresh(new_renta)

    valores_nuevos = {column.name: getattr(new_renta, column.name) for column in new_renta.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "renta",
        new_renta.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_renta

def add_propiedad_to_renta(db: Session, renta_id: int, propiedad_id: int, user: User = None):
    renta = db.query(Renta).filter(Renta.id == renta_id).first()
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    renta.propiedades.append(propiedad)
    db.commit()
    db.refresh(renta)

    valores_nuevos = {column.name: getattr(renta, column.name) for column in renta.__table__.columns}

    create_auditoria(
        db,
        "AGREGAR",
        "renta",
        renta.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return renta

def remove_propiedad_from_renta(db: Session, renta_id: int, propiedad_id: int, user: User = None):
    renta = db.query(Renta).filter(Renta.id == renta_id).first()
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    renta.propiedades.remove(propiedad)
    db.commit()
    db.refresh(renta)

    valores_anteriores = {column.name: getattr(renta, column.name) for column in renta.__table__.columns}

    create_auditoria(
        db,
        "QUITAR",
        "renta",
        renta.id,
        user.username if user else None,
        valores_anteriores,
        None,
    )

    return renta

def update_renta(db: Session, renta_id: int, renta: RentaCreate, user: User = None):
    # db.query(Renta).filter(Renta.id == renta_id).update(renta.dict())
    # db.commit()
    # return db.query(Renta).filter(Renta.id == renta_id).first()
    existing_renta = db.query(Renta).filter(Renta.id == renta_id).first()
    valores_anteriores = {column.name: getattr(existing_renta, column.name) for column in existing_renta.__table__.columns}

    db.query(Renta).filter(Renta.id == renta_id).update(renta.dict())
    db.commit()
    updated_renta = db.query(Renta).filter(Renta.id == renta_id).first()

    valores_nuevos = {column.name: getattr(updated_renta, column.name) for column in updated_renta.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "renta",
        updated_renta.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_renta

def delete_renta(db: Session, renta_id: int, user: User = None):
    renta = db.query(Renta).filter(Renta.id == renta_id).first()
    if renta:
        valores_anteriores = {column.name: getattr(renta, column.name) for column in renta.__table__.columns}

        db.delete(renta)
        db.commit()

        create_auditoria(
            db,
            "ELIMINAR",
            "renta",
            renta.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
    return renta