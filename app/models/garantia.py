from app.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, Date, TIMESTAMP, func
from app.models.propiedad import garantia_propiedad

class Garantia(Base):
    __tablename__ = "garantia"

    id = Column(Integer, primary_key=True, index=True)
    beneficiario = Column(String(255), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    propiedades = relationship("Propiedad", secondary=garantia_propiedad, back_populates="garantias")
