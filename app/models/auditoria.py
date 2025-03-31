from app.config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, JSON

class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)
    operacion = Column(String(255), nullable=False)
    tabla_afectada = Column(String(255), nullable=False)
    registro_tabla_id = Column(Integer, nullable=False)
    usuario_username = Column(String(255), nullable=False)
    valores_anteriores = Column(JSON, nullable=True)
    valores_nuevos = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
