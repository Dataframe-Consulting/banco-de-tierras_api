from sqlalchemy.orm import Session
from app.models.vocacion_especifica import VocacionEspecifica
from app.schemas.vocacion_especifica import VocacionEspecificaCreate
import math
from app.models.user import User
from app.services.auditoria import create_auditoria

def get_all_vocaciones_especificas_without_pagination(db: Session):
    return db.query(VocacionEspecifica).all()

def get_all_vocaciones_especificas(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(VocacionEspecifica)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    vocaciones_especificas = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": vocaciones_especificas
    }

def get_vocacion_especifica_by_id(db: Session, vocacion_especifica_id: int):
    return db.query(VocacionEspecifica).filter(VocacionEspecifica.id == vocacion_especifica_id).first()

def get_vocacion_especifica_by_valor(db: Session, valor: str):
    return db.query(VocacionEspecifica).filter(VocacionEspecifica.valor == valor).first()

def create_vocacion_especifica(db: Session, vocacion_especifica: VocacionEspecificaCreate, user: User = None):
    new_vocacion_especifica = VocacionEspecifica(**vocacion_especifica.dict())
    db.add(new_vocacion_especifica)
    db.commit()
    db.refresh(new_vocacion_especifica)

    valores_nuevos = {column.name: getattr(new_vocacion_especifica, column.name) for column in new_vocacion_especifica.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "vocacion_especifica",
        new_vocacion_especifica.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_vocacion_especifica

def update_vocacion_especifica(db: Session, vocacion_especifica_id: int, vocacion_especifica: VocacionEspecificaCreate, user: User = None):
    existing_vocacion_especifica = db.query(VocacionEspecifica).filter(VocacionEspecifica.id == vocacion_especifica_id).first()
    valores_anteriores = {column.name: getattr(existing_vocacion_especifica, column.name) for column in VocacionEspecifica.__table__.columns}

    db.query(VocacionEspecifica).filter(VocacionEspecifica.id == vocacion_especifica_id).update(vocacion_especifica.dict())
    db.commit()
    updated_vocacion_especifica = db.query(VocacionEspecifica).filter(VocacionEspecifica.id == vocacion_especifica_id).first()

    valores_nuevos = {column.name: getattr(updated_vocacion_especifica, column.name) for column in VocacionEspecifica.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "vocacion_especifica",
        updated_vocacion_especifica.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_vocacion_especifica

def delete_vocacion_especifica(db: Session, vocacion_especifica_id: int, user: User = None):
    vocacion_especifica = db.query(VocacionEspecifica).filter(VocacionEspecifica.id == vocacion_especifica_id).first()
    if vocacion_especifica:
        valores_anteriores = {column.name: getattr(vocacion_especifica, column.name) for column in VocacionEspecifica.__table__.columns}
        db.delete(vocacion_especifica)
        db.commit()

        create_auditoria(
            db,
            "ELIMINAR",
            "vocacion_especifica",
            vocacion_especifica.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
    return vocacion_especifica