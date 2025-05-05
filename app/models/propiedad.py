from app.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, Boolean, String, Text, TIMESTAMP, func, Table, ForeignKey
from app.models.renta import propiedad_renta

class PropietarioPropiedad(Base):
    __tablename__ = "propietario_propiedad"

    es_socio = Column(Boolean, nullable=False)
    sociedad_porcentaje_participacion = Column(Float, nullable=False)
    propietario_id = Column(Integer, ForeignKey("propietario.id", ondelete="CASCADE"), primary_key=True)
    propiedad_id = Column(Integer, ForeignKey("propiedad.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    propietario = relationship("Propietario", back_populates="propiedades")
    propiedad = relationship("Propiedad", back_populates="propietarios")

ubicacion_propiedad = Table(
    "ubicacion_propiedad",
    Base.metadata,
    Column("ubicacion_id", ForeignKey("ubicacion.id", ondelete="CASCADE"), primary_key=True),
    Column("propiedad_id", ForeignKey("propiedad.id", ondelete="CASCADE"), primary_key=True)
)

garantia_propiedad = Table(
    "garantia_propiedad",
    Base.metadata,
    Column("garantia_id", ForeignKey("garantia.id", ondelete="CASCADE"), primary_key=True),
    Column("propiedad_id", ForeignKey("propiedad.id", ondelete="CASCADE"), primary_key=True)
)

proceso_legal_propiedad = Table(
    "proceso_legal_propiedad",
    Base.metadata,
    Column("proceso_legal_id", ForeignKey("proceso_legal.id", ondelete="CASCADE"), primary_key=True),
    Column("propiedad_id", ForeignKey("propiedad.id", ondelete="CASCADE"), primary_key=True)
)

class Propiedad(Base):
    __tablename__ = "propiedad"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    superficie = Column(Float, nullable=False)
    valor_comercial = Column(Float, nullable=False)
    anio_valor_comercial = Column(Integer, nullable=True)
    clave_catastral = Column(String(255), unique=True, nullable=False)
    base_predial = Column(Float, nullable=False)
    adeudo_predial = Column(Float, nullable=True)
    anios_pend_predial = Column(Integer, nullable=True)
    comentarios = Column(Text, nullable=True)
    proyecto_id = Column(Integer, ForeignKey("proyecto.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    proyecto = relationship("Proyecto", back_populates="propiedades")
    propietarios = relationship("PropietarioPropiedad", back_populates="propiedad")
    ubicaciones = relationship("Ubicacion", secondary=ubicacion_propiedad, back_populates="propiedades")
    garantias = relationship("Garantia", secondary=garantia_propiedad, back_populates="propiedades")
    procesos_legales = relationship("ProcesoLegal", secondary=proceso_legal_propiedad, back_populates="propiedades")
    rentas = relationship("Renta", secondary=propiedad_renta, back_populates="propiedades")
    archivos = relationship("Archivo", back_populates="propiedad")