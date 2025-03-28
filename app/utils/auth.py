from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.settings import settings
from datetime import datetime, timedelta
from app.utils.bcrypt import verify_password
from app.services.user import get_user_by_username
from fastapi import Depends, HTTPException, status, Cookie, Header

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user(
    access_token: str = Cookie(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if access_token is None and authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó un token de acceso",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = (access_token or authorization).replace("Bearer ", "").strip(' "')

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
