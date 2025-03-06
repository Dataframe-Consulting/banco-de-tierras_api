from app.config.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.proyecto import propietario_proyecto

propietario_socio_table = Table(
    "propietario_socio",
    Base.metadata,
    Column("propietario_id", Integer, ForeignKey("propietario.id", ondelete="CASCADE"), primary_key=True),
    Column("socio_id", Integer, ForeignKey("socio.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", TIMESTAMP, server_default=func.current_timestamp()),
)

class Propietario(Base):
    __tablename__ = "propietario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    rfc = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    proyectos = relationship("Proyecto", secondary=propietario_proyecto, back_populates="propietarios")
    socios = relationship("Socio", secondary=propietario_socio_table, back_populates="propietarios")