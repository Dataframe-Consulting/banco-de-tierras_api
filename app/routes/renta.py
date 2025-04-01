from typing import List, Optional
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.schemas.renta import RentaCreate, RentaResponse, PaginatedRentasResponse
from app.services.renta import get_all_rentas, get_all_rentas_without_pagination, get_renta_by_id, create_renta, add_propiedad_to_renta, remove_propiedad_from_renta, update_renta, delete_renta
from app.services.propiedad import get_propiedad_by_id

router = APIRouter(prefix="/renta", tags=["Rentas"])

# WITH PAGINATION
# @router.get("/", response_model=PaginatedRentasResponse)
# def get_rentas(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
#     return get_all_rentas(db, page, page_size)

# WITHOUT PAGINATION
@router.get("/", response_model=List[RentaResponse])
def get_rentas(
    db: Session = Depends(get_db), 
    q: Optional[str] = Query(None, description="Busca por nombre comercial o razon social..."),
    propiedad_id: Optional[int] = Query(None, description="Filtrar por ID de propiedad"),
):
    return get_all_rentas_without_pagination(db, q, propiedad_id)

@router.get("/{renta_id}", response_model=RentaResponse)
def get_renta(renta_id: int, db: Session = Depends(get_db)):
    db_renta = get_renta_by_id(db, renta_id)
    if not db_renta:
        raise HTTPException(status_code=404, detail="Renta no encontrada")
    return db_renta

@router.post("/", response_model=RentaResponse)
def create_new_renta(renta: RentaCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_renta(db, renta, user)

@router.post("/{renta_id}/propiedad/{propiedad_id}", response_model=RentaResponse)
def add_propiedad_to_some_renta(renta_id: int, propiedad_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_renta = get_renta_by_id(db, renta_id)
    if not db_renta:
        raise HTTPException(status_code=404, detail="Renta no encontrada")
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    propiedad_already_added = any(db_propiedad.id == propiedad.id for propiedad in db_renta.propiedades)
    if propiedad_already_added:
        raise HTTPException(status_code=400, detail="Propiedad ya agregada a la renta")
    return add_propiedad_to_renta(db, renta_id, propiedad_id, user)

@router.delete("/{renta_id}/propiedad/{propiedad_id}", response_model=RentaResponse)
def remove_propiedad_from_some_renta(renta_id: int, propiedad_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_renta = get_renta_by_id(db, renta_id)
    if not db_renta:
        raise HTTPException(status_code=404, detail="Renta no encontrada")
    db_propiedad = get_propiedad_by_id(db, propiedad_id)
    if not db_propiedad:
        raise HTTPException(status_code=404, detail="Propiedad no encontrada")
    propiedad_not_added = all(db_propiedad.id != propiedad.id for propiedad in db_renta.propiedades)
    if propiedad_not_added:
        raise HTTPException(status_code=400, detail="Propiedad no agregada a la renta")
    return remove_propiedad_from_renta(db, renta_id, propiedad_id, user)

@router.put("/{renta_id}", response_model=RentaResponse)
def update_renta_by_id(renta_id: int, renta: RentaCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_renta = get_renta_by_id(db, renta_id)
    if not db_renta:
        raise HTTPException(status_code=404, detail="Renta no encontrada")
    return update_renta(db, renta_id, renta, user)

@router.delete("/{renta_id}", response_model=RentaResponse)
def delete_renta_by_id(renta_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_renta = get_renta_by_id(db, renta_id)
    if not db_renta:
        raise HTTPException(status_code=404, detail="Renta no encontrada")
    return delete_renta(db, renta_id, user)