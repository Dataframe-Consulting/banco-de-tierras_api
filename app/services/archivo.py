from sqlalchemy.orm import Session
from app.models.user import User
from app.models.archivo import Archivo

from app.services.auditoria import create_auditoria

def create_file(db: Session, tabla_nombre: str, tabla_id: int, url: str, user: User = None):
    if tabla_nombre == "proyecto":
        new_file = Archivo(url=url, proyecto_id=tabla_id, )
    elif tabla_nombre == "propiedad":
        new_file = Archivo(url=url, propiedad_id=tabla_id, )
    elif tabla_nombre == "propietario":
        new_file = Archivo(url=url, propietario_id=tabla_id, )
    elif tabla_nombre == "garantia":
        new_file = Archivo(url=url, garantia_id=tabla_id, )
    else:
        new_file = Archivo(url=url, proceso_legal_id=tabla_id, )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    # Log the creation of the new file
    valores_nuevos = {column.name: getattr(new_file, column.name) for column in new_file.__table__.columns}

    auditoria = create_auditoria(
        db,
        "CREAR",
        "archivo",
        new_file.id,
        user.username if user else None,
        None,
        valores_nuevos,
    )
    # Log the creation of the new file

    return new_file

def get_file(db: Session, file_id: int):
    return db.query(Archivo).filter(Archivo.id == file_id).first()

def delete_file(db: Session, file_id: int, user: User = None):
    file = db.query(Archivo).filter(Archivo.id == file_id).first()
    if file:
        # Log the deletion of the file
        valores_anteriores = {column.name: getattr(file, column.name) for column in file.__table__.columns}
        # Log the deletion of the file

        db.delete(file)
        db.commit()

        # Log the deletion of the file
        auditoria = create_auditoria(
            db,
            "ELIMINAR",
            "archivo",
            file.id,
            user.username if user else None,
            valores_anteriores,
            None,
        )
        # Log the deletion of the file

    return file