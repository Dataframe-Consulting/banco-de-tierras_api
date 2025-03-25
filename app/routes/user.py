from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.settings import settings
from app.schemas.user import UserCreate
from app.services.user import create_user, get_user_by_username, get_user_by_email
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.utils.auth import create_access_token, authenticate_user, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user_by_username = get_user_by_username(db, user.username)
    if existing_user_by_username:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    existing_user_by_email = get_user_by_email(db, user.email)
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="El email ya existe")
    return create_user(db, user)

@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    access_token = create_access_token({"sub": user.username})

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="Strict",
        domain=".banco-de-tierras.vercel.app" if settings.ENV == "production" else "localhost"
    )
    return {"message": "Login exitoso"}

@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return {"username": user.username, "email": user.email}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout exitoso"}