from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.propiedad import get_propiedad_by_id
from app.schemas.garantia import GarantiaCreate, GarantiaResponse, PaginatedGarantiasResponse
from app.services.garantia import get_all_garantias, get_all_garantias_without_pagination, get_garantia_by_id, create_garantia, update_garantia, delete_garantia
from app.utils.auth import get_current_user

router = APIRouter(prefix="/garantia", tags=["Garantias"])

# WITH PAGINATION
# @router.get("/", response_model=PaginatedGarantiasResponse)
# def get_garantias(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_garantias(db, page, page_size)

# WITHOUT PAGINATION
@router.get("/", response_model=List[GarantiaResponse])
def get_garantias(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Busca por beneficiario..."),
    propiedad_id: Optional[int] = Query(None, description="Filtrar por ID de propiedad")
):
    return get_all_garantias_without_pagination(db, q,  propiedad_id)

@router.get("/{garantia_id}", response_model=GarantiaResponse)
def get_garantia(garantia_id: int, db: Session = Depends(get_db)):
    db_garantia = get_garantia_by_id(db, garantia_id)
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantia no encontrada")
    return db_garantia

@router.post("/", response_model=GarantiaResponse)
def create_new_garantia(garantia: GarantiaCreate, db: Session = Depends(get_db)):
    db_propiedad = get_propiedad_by_id(db, garantia.propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return create_garantia(db, garantia)

@router.put("/{garantia_id}", response_model=GarantiaResponse)
def update_existing_garantia(garantia_id: int, garantia: GarantiaCreate, db: Session = Depends(get_db)):
    db_garantia = get_garantia_by_id(db, garantia_id)
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantia no encontrada")
    db_propiedad = get_propiedad_by_id(db, garantia.propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    return update_garantia(db, garantia_id, garantia)

@router.delete("/{garantia_id}", response_model=GarantiaResponse)
def delete_existing_garantia(garantia_id: int, db: Session = Depends(get_db)):
    db_garantia = get_garantia_by_id(db, garantia_id)
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantia no encontrada")
    return delete_garantia(db, garantia_id)