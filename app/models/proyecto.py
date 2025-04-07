from app.config.database import Base
from sqlalchemy import Column, Integer, Float, Boolean, String, Text, TIMESTAMP, func, Table, ForeignKey
from sqlalchemy.orm import relationship

propietario_proyecto = Table(
    "propietario_proyecto",
    Base.metadata,
    Column("propietario_id", ForeignKey("propietario.id", ondelete="CASCADE"), primary_key=True),
    Column("proyecto_id", ForeignKey("proyecto.id", ondelete="CASCADE"), primary_key=True)
)

class Proyecto(Base):
    __tablename__ = "proyecto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, nullable=False)
    superficie_total = Column(Float, nullable=False)
    esta_activo = Column(Boolean, nullable=True, default=True)
    comentarios = Column(Text, nullable=True)
    situacion_fisica_id = Column(Integer, ForeignKey("situacion_fisica.id", ondelete="CASCADE"), nullable=False)
    vocacion_id = Column(Integer, ForeignKey("vocacion.id", ondelete="CASCADE"), nullable=False)
    vocacion_especifica_id = Column(Integer, ForeignKey("vocacion_especifica.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    situacion_fisica = relationship("SituacionFisica", back_populates="proyectos")
    vocacion = relationship("Vocacion", back_populates="proyectos")
    vocacion_especifica = relationship("VocacionEspecifica", back_populates="proyectos")

    propietarios = relationship("Propietario", secondary=propietario_proyecto, back_populates="proyectos")
    propiedades = relationship("Propiedad", back_populates="proyecto")