from sqlalchemy.orm import Session
from app.models.vocacion_especifica import VocacionEspecifica
from app.schemas.vocacion_especifica import VocacionEspecificaCreate
import math

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

def create_vocacion_especifica(db: Session, vocacion_especifica: VocacionEspecificaCreate):
    new_vocacion_especifica = VocacionEspecifica(**vocacion_especifica.dict())
    db.add(new_vocacion_especifica)
    db.commit()
    db.refresh(new_vocacion_especifica)
    return new_vocacion_especifica

def update_vocacion_especifica(db: Session, vocacion_especifica_id: int, vocacion_especifica: VocacionEspecificaCreate):
    db.query(VocacionEspecifica).filter(VocacionEspecifica.id == vocacion_especifica_id).update(vocacion_especifica.dict())
    db.commit()
    return db.query(VocacionEspecifica).filter(VocacionEspecifica.id == vocacion_especifica_id).first()

def delete_vocacion_especifica(db: Session, vocacion_especifica_id: int):
    vocacion_especifica = db.query(VocacionEspecifica).filter(VocacionEspecifica.id == vocacion_especifica_id).first()
    if vocacion_especifica:
        db.delete(vocacion_especifica)
        db.commit()
    return vocacion_especifica