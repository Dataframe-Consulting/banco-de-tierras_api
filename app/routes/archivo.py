from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.config.database import get_db

from app.models.user import User
from app.utils.auth import get_current_user

from app.schemas.archivo import ArchivoResponse, ArchivoCreate
from app.services.archivo import create_file, get_file, delete_file

from app.services.proyecto import get_proyecto_by_id
from app.services.propiedad import get_propiedad_by_id
from app.services.propietario import get_propietario_by_id
from app.services.garantia import get_garantia_by_id
from app.services.proceso_legal import get_proceso_legal_by_id

router = APIRouter(prefix="/archivo", tags=["Archivos"])

@router.post("/tabla/{tabla_nombre}/id/{tabla_id}", response_model=ArchivoResponse)
def create_new_file(
    tabla_nombre: str,
    tabla_id: int,
    archivoUrl: ArchivoCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    url = archivoUrl.url
    if tabla_nombre == "proyecto":
        db_proyecto = get_proyecto_by_id(db, tabla_id)
        if not db_proyecto:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    elif tabla_nombre == "propiedad":
        db_propiedad = get_propiedad_by_id(db, tabla_id)
        if not db_propiedad:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    elif tabla_nombre == "propietario":
        db_propietario = get_propietario_by_id(db, tabla_id)
        if not db_propietario:
            raise HTTPException(status_code=404, detail="Propietario no encontrado")
    elif tabla_nombre == "garantia":
        db_garantia = get_garantia_by_id(db, tabla_id)
        if not db_garantia:
            raise HTTPException(status_code=404, detail="Garantia no encontrada")
    elif tabla_nombre == "proceso_legal":
        db_proceso_legal = get_proceso_legal_by_id(db, tabla_id)
        if not db_proceso_legal:
            raise HTTPException(status_code=404, detail="Proceso legal no encontrado")
    else:
        raise HTTPException(status_code=400, detail="Tabla no válida")
    return create_file(db, tabla_nombre, tabla_id, url, user)

@router.delete("/{file_id}", response_model=ArchivoResponse)
def delete_existing_file(
    file_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_file = get_file(db, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return delete_file(db, file_id, user)