from app.config.database import Base
from sqlalchemy import Column, Integer, Float, Boolean, String, Text, Date, TIMESTAMP, func, Table, ForeignKey
from sqlalchemy.orm import relationship

class ProcesoLegal(Base):
    __tablename__ = "proceso_legal"

    id = Column(Integer, primary_key=True, index=True)
    abogado = Column(String(255), nullable=False)
    tipo_proceso = Column(String(255), nullable=False)
    estatus = Column(String(255), nullable=False)
    propiedad_id = Column(Integer, ForeignKey("propiedad.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    propiedad = relationship("Propiedad", back_populates="procesos_legales")
