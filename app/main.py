from fastapi import FastAPI, Depends
from app.config.settings import settings
from app.utils.auth import get_current_user
from app.config.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, situacion_fisica, vocacion, vocacion_especifica, proyecto, propietario, ubicacion, garantia, proceso_legal, propiedad, renta, auditoria, archivo

app = FastAPI(
    title="Banco de Tierras API", 
    description="Descripción de mi API",
    version="1.0.0",
    secret_key=settings.SECRET_KEY,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(f"{settings.API_PREFIX}/health")
def health_check():
    return {"status": "ok"}

Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix=settings.API_PREFIX)
app.include_router(situacion_fisica.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(vocacion.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(vocacion_especifica.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(proyecto.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(propietario.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(ubicacion.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(garantia.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(proceso_legal.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(propiedad.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(renta.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(auditoria.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])
app.include_router(archivo.router, prefix=settings.API_PREFIX, dependencies=[Depends(get_current_user)])