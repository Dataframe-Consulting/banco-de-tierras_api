from app.config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.models.propietario import propietario_socio_table

class Socio(Base):
    __tablename__ = "socio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    propietarios = relationship("Propietario", secondary=propietario_socio_table, back_populates="socios")