from app.config.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, func

from app.models.proyecto import propietario_proyecto

class Propietario(Base):
    __tablename__ = "propietario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    rfc = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    proyectos = relationship("Proyecto", secondary=propietario_proyecto, back_populates="propietarios")
    propiedades = relationship("PropietarioSociedadPropiedad", back_populates="propietario")