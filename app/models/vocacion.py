from app.config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Table, ForeignKey
from sqlalchemy.orm import relationship

class Vocacion(Base):
    __tablename__ = "vocacion"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    proyectos = relationship("Proyecto", back_populates="vocacion")