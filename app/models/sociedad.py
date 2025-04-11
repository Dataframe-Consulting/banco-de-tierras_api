from app.config.database import Base
from sqlalchemy import Column, Integer, Float, TIMESTAMP, func
from sqlalchemy.orm import relationship

class Sociedad(Base):
    __tablename__ = "sociedad"

    id = Column(Integer, primary_key=True, index=True)
    porcentaje_participacion = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    propiedades = relationship("PropietarioSociedadPropiedad", back_populates="sociedad")