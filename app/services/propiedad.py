import math
from sqlalchemy.orm import Session, joinedload

from app.models.propiedad import Propiedad, PropietarioPropiedad

from app.models.user import User

from app.models.garantia import Garantia
from app.models.ubicacion import Ubicacion
from app.schemas.propiedad import PropiedadCreate
from app.models.proceso_legal import ProcesoLegal
from app.services.auditoria import create_auditoria

def get_all_propiedades_without_pagination(
    db: Session,
    q: str = None,
    proyecto_id: int = None,
    ubicacion_id: int = None,
    garantia_id: int = None,
    proceso_legal_id: int = None
):
    query = db.query(Propiedad)

    if q:
        query = query.filter(Propiedad.nombre.ilike(f"%{q}%"))

    if proyecto_id:
        query = query.filter(Propiedad.proyecto_id == proyecto_id)

    if ubicacion_id:
        query = query.join(Propiedad.ubicaciones).filter(Ubicacion.id == ubicacion_id)

    if garantia_id:
        query = query.join(Propiedad.garantias).filter(Garantia.id == garantia_id)

    if proceso_legal_id:
        query = query.join(Propiedad.procesos_legales).filter(ProcesoLegal.id == proceso_legal_id)

    return query.all()

def get_all_propiedades(db: Session, page: int = 1, page_size: int = 10):
    query = db.query(Propiedad)
    total = query.count()

    total_pages = math.ceil(total / page_size) if total > 0 else 1
    skip = (page - 1) * page_size
    propiedades = query.offset(skip).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": propiedades
    }

def get_propiedad_by_id(db: Session, propiedad_id: int):
    return db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()

def get_propiedad_by_nombre(db: Session, nombre: str):
    return db.query(Propiedad).filter(Propiedad.nombre == nombre).first()

def get_propiedad_by_clave_catastral(db: Session, clave_catastral: str):
    return db.query(Propiedad).filter(Propiedad.clave_catastral == clave_catastral).first()

def create_propiedad(db: Session, propiedad: PropiedadCreate, user: User = None):
    new_propiedad = Propiedad(**propiedad.dict())
    db.add(new_propiedad)
    db.commit()
    db.refresh(new_propiedad)

    valores_nuevos = {column.name: getattr(new_propiedad, column.name) for column in new_propiedad.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "propiedad",
        new_propiedad.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )

    return new_propiedad

def check_propietario_in_propiedad(db: Session, propiedad_id: int, propietario_id: int):
    return db.query(PropietarioPropiedad).filter(
        PropietarioPropiedad.propiedad_id == propiedad_id,
        PropietarioPropiedad.propietario_id == propietario_id
    ).first()

def add_propietario_to_propiedad(db: Session, propiedad_id: int, propietario_id: int, sociedad_porcentaje_participacion: float, es_socio: bool, user: User = None):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    propietario_propiedad = PropietarioPropiedad(
        es_socio=es_socio,
        sociedad_porcentaje_participacion=sociedad_porcentaje_participacion,
        propietario_id=propietario_id,
        propiedad_id=propiedad_id
    )
    propiedad.propietarios.append(propietario_propiedad)
    db.commit()
    db.refresh(propiedad)

    valores_nuevos = {column.name: getattr(propietario_propiedad, column.name) for column in propietario_propiedad.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "propietario_propiedad",
        f"{propietario_id}_{propiedad_id}",
        user.username if user else None,
        None,
        valores_nuevos
    )

    return propiedad

def remove_propietario_from_propiedad(db: Session, propiedad_id: int, propietario_id: int, user: User = None):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    propietario_propiedad = db.query(PropietarioPropiedad).filter(
        PropietarioPropiedad.propiedad_id == propiedad_id,
        PropietarioPropiedad.propietario_id == propietario_id
    ).first()

    if propietario_propiedad:
        db.delete(propietario_propiedad)
        db.commit()
        db.refresh(propiedad)

        valores_anteriores = {column.name: getattr(propietario_propiedad, column.name) for column in propietario_propiedad.__table__.columns}

        create_auditoria(
            db,
            "ELIMINAR",
            "propietario_propiedad",
            f"{propietario_id}_{propiedad_id}",
            user.username if user else None,
            valores_anteriores,
            None
        )

    return propiedad

def add_ubicacion_to_propiedad(db: Session, propiedad_id: int, ubicacion_id: int, user: User = None):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    propiedad.ubicaciones.append(ubicacion)
    db.commit()
    db.refresh(propiedad)

    valores_nuevos = {column.name: getattr(ubicacion, column.name) for column in ubicacion.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "ubicacion_propiedad",
        ubicacion.id,
        user.username if user else None,
        None,
        valores_nuevos
    )

    return propiedad

def remove_ubicacion_from_propiedad(db: Session, propiedad_id: int, ubicacion_id: int, user: User = None):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    propiedad.ubicaciones.remove(ubicacion)
    db.commit()
    db.refresh(propiedad)

    valores_anteriores = {column.name: getattr(ubicacion, column.name) for column in ubicacion.__table__.columns}

    create_auditoria(
        db,
        "ELIMINAR",
        "ubicacion_propiedad",
        ubicacion.id,
        user.username if user else None,
        valores_anteriores,
        None
    )

    return propiedad

def add_garantia_to_propiedad(db: Session, propiedad_id: int, garantia_id: int, user: User = None):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    garantia = db.query(Garantia).filter(Garantia.id == garantia_id).first()
    propiedad.garantias.append(garantia)
    db.commit()
    db.refresh(propiedad)

    valores_nuevos = {column.name: getattr(garantia, column.name) for column in garantia.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "garantia_propiedad",
        garantia.id,
        user.username if user else None,
        None,
        valores_nuevos
    )

    return propiedad

def remove_garantia_from_propiedad(db: Session, propiedad_id: int, garantia_id: int, user: User = None):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    garantia = db.query(Garantia).filter(Garantia.id == garantia_id).first()
    propiedad.garantias.remove(garantia)
    db.commit()
    db.refresh(propiedad)

    valores_anteriores = {column.name: getattr(garantia, column.name) for column in garantia.__table__.columns}

    create_auditoria(
        db,
        "ELIMINAR",
        "garantia_propiedad",
        garantia.id,
        user.username if user else None,
        valores_anteriores,
        None
    )

    return propiedad

def add_proceso_legal_to_propiedad(db: Session, propiedad_id: int, proceso_legal_id: int, user: User = None):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    proceso_legal = db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).first()
    propiedad.procesos_legales.append(proceso_legal)
    db.commit()
    db.refresh(propiedad)

    valores_nuevos = {column.name: getattr(proceso_legal, column.name) for column in proceso_legal.__table__.columns}

    create_auditoria(
        db,
        "CREAR",
        "proceso_legal_propiedad",
        proceso_legal.id,
        user.username if user else None,
        None,
        valores_nuevos
    )

    return propiedad

def remove_proceso_legal_from_propiedad(db: Session, propiedad_id: int, proceso_legal_id: int, user: User = None):
    propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    proceso_legal = db.query(ProcesoLegal).filter(ProcesoLegal.id == proceso_legal_id).first()
    propiedad.procesos_legales.remove(proceso_legal)
    db.commit()
    db.refresh(propiedad)

    valores_anteriores = {column.name: getattr(proceso_legal, column.name) for column in proceso_legal.__table__.columns}

    create_auditoria(
        db,
        "ELIMINAR",
        "proceso_legal_propiedad",
        proceso_legal.id,
        user.username if user else None,
        valores_anteriores,
        None
    )

    return propiedad

def update_propiedad(db: Session, propiedad_id: int, propiedad: PropiedadCreate, user: User = None):
    existing_propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
    valores_anteriores = {column.name: getattr(existing_propiedad, column.name) for column in existing_propiedad.__table__.columns}

    db.query(Propiedad).filter(Propiedad.id == propiedad_id).update(propiedad.dict())
    db.commit()
    updated_propiedad = db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()

    valores_nuevos = {column.name: getattr(updated_propiedad, column.name) for column in updated_propiedad.__table__.columns}

    create_auditoria(
        db,
        "EDITAR",
        "propiedad",
        updated_propiedad.id,
        user.username if user else None,
        valores_anteriores,
        valores_nuevos,
    )

    return updated_propiedad

def delete_propiedad(db: Session, propiedad_id: int, user: User = None):
    db.query(PropietarioPropiedad).filter(PropietarioPropiedad.propiedad_id == propiedad_id).delete()
    db.commit()

    propiedad = db.query(Propiedad).options(
        joinedload(Propiedad.proyecto)
    ).filter(Propiedad.id == propiedad_id).first()
    if propiedad:
        valores_anteriores = {column.name: getattr(propiedad, column.name) for column in propiedad.__table__.columns}

        db.delete(propiedad)
        db.commit()

        create_auditoria(
            db,
            "ELIMINAR",
            "propiedad",
            propiedad.id,
            user.username if user else None,
            valores_anteriores,
            None
        )
    return propiedad