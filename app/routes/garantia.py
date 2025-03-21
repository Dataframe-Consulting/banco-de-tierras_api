from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query

from app.config.database import get_db

from app.models.user import User
from app.utils.auth import get_current_user

from app.schemas.garantia import GarantiaCreate, GarantiaResponse
from app.services.garantia import get_all_garantias_without_pagination, get_garantia_by_id, create_garantia, update_garantia, delete_garantia

router = APIRouter(prefix="/garantia", tags=["Garantias"])

@router.get("/", response_model=List[GarantiaResponse])
def get_garantias(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(None, description="Busca por beneficiario...")
):
    return get_all_garantias_without_pagination(db, q)

@router.get("/{garantia_id}", response_model=GarantiaResponse)
def get_garantia(garantia_id: int, db: Session = Depends(get_db)):
    db_garantia = get_garantia_by_id(db, garantia_id)
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantia no encontrada")
    return db_garantia

@router.post("/", response_model=GarantiaResponse)
def create_new_garantia(garantia: GarantiaCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_garantia(db, garantia, user)

@router.put("/{garantia_id}", response_model=GarantiaResponse)
def update_existing_garantia(garantia_id: int, garantia: GarantiaCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_garantia = get_garantia_by_id(db, garantia_id)
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantia no encontrada")
    return update_garantia(db, garantia_id, garantia, user)

@router.delete("/{garantia_id}", response_model=GarantiaResponse)
def delete_existing_garantia(garantia_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_garantia = get_garantia_by_id(db, garantia_id)
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantia no encontrada")
    return delete_garantia(db, garantia_id, user)