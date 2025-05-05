from app.config.database import Base
from sqlalchemy import Column, Integer, Float, Boolean, String, Text, Date, TIMESTAMP, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.propiedad import proceso_legal_propiedad

class ProcesoLegal(Base):
    __tablename__ = "proceso_legal"

    id = Column(Integer, primary_key=True, index=True)
    abogado = Column(String(255), nullable=False)
    tipo_proceso = Column(String(255), nullable=False)
    estatus = Column(String(255), nullable=False)
    comentarios = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    propiedades = relationship("Propiedad", secondary=proceso_legal_propiedad, back_populates="procesos_legales")
    archivos = relationship("Archivo", back_populates="proceso_legal")
