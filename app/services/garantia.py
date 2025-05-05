import math
from sqlalchemy.orm import Session

from app.models.user import User

from app.models.garantia import Garantia
from app.schemas.garantia import GarantiaCreate
from app.services.auditoria import create_auditoria
from app.models.archivo import Archivo

def get_all_garantias_without_pagination(
    db: Session,
    q: str = None,
):
    query = db.query(Garantia)

    if(q):
        query = query.filter(Garantia.beneficiario.ilike(f"%{q}%"))

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

def create_garantia(db: Session, garantia: GarantiaCreate, user: User = None):
    new_garantia = Garantia(**garantia.dict())
    db.add(new_garantia)
    db.commit()
    db.refresh(new_garantia)

    # Log the creation of the new garantia
    valores_nuevos = {column.name: getattr(new_garantia, column.name) for column in new_garantia.__table__.columns}

    auditoria = create_auditoria(
        db,
        "CREAR",
        "garantia",
        new_garantia.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )
    # Log the creation of the new garantia

    return new_garantia

def update_garantia(db: Session, garantia_id: int, garantia: GarantiaCreate, user: User = None):
    # Log the update of the garantia
    existing_garantia = db.query(Garantia).filter(Garantia.id == garantia_id).first()
    valores_anteriores = {column.name: getattr(existing_garantia, column.name) for column in existing_garantia.__table__.columns}
    # Log the update of the garantia

    db.query(Garantia).filter(Garantia.id == garantia_id).update(garantia.dict())
    db.commit()
    updated_garantia = db.query(Garantia).filter(Garantia.id == garantia_id).first()

    # Log the update of the garantia
    valores_nuevos = {column.name: getattr(updated_garantia, column.name) for column in updated_garantia.__table__.columns}

    auditoria = create_auditoria(
        db,
        "EDITAR",
        "garantia",
        updated_garantia.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )
    # Log the update of the garantia

    return updated_garantia

def delete_garantia(db: Session, garantia_id: int, user: User = None):
    db.query(Archivo).filter(Archivo.garantia_id == garantia_id).delete()

    garantia = db.query(Garantia).filter(Garantia.id == garantia_id).first()
    if garantia:
        # Log the deletion of the garantia
        valores_anteriores = {column.name: getattr(garantia, column.name) for column in garantia.__table__.columns}
        # Log the deletion of the garantia

        db.delete(garantia)
        db.commit()

        # Log the deletion of the garantia
        create_auditoria(
            db,
            "ELIMINAR",
            "garantia",
            garantia.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
        # Log the deletion of the garantia
    return garantia