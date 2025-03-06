from app.config.database import Base
from sqlalchemy import Column, Integer, Float, Boolean, String, Text, TIMESTAMP, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.propiedad import ubicacion_propiedad

class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    propiedades = relationship("Propiedad", secondary=ubicacion_propiedad, back_populates="ubicaciones")