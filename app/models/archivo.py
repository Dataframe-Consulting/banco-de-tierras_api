from app.config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship

class Archivo(Base):
    __tablename__ = "archivo"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    proyecto_id = Column(Integer, ForeignKey("proyecto.id"), nullable=True)
    propiedad_id = Column(Integer, ForeignKey("propiedad.id"), nullable=True)
    propietario_id = Column(Integer, ForeignKey("propietario.id"), nullable=True)
    garantia_id = Column(Integer, ForeignKey("garantia.id"), nullable=True)
    proceso_legal_id = Column(Integer, ForeignKey("proceso_legal.id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    proyecto = relationship("Proyecto", back_populates="archivos")
    propiedad = relationship("Propiedad", back_populates="archivos")
    propietario = relationship("Propietario", back_populates="archivos")
    garantia = relationship("Garantia", back_populates="archivos")
    proceso_legal = relationship("ProcesoLegal", back_populates="archivos")