from app.config.database import Base
from sqlalchemy import Column, Integer, Float, String, TIMESTAMP, func, Table, ForeignKey
from sqlalchemy.orm import relationship

class SituacionFisica(Base):
    __tablename__ = "situacion_fisica"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    proyectos = relationship("Proyecto", back_populates="situacion_fisica")