from app.config.database import Base
from sqlalchemy import Column, Integer, Float, Boolean, String, Text, Date, TIMESTAMP, func, Table, ForeignKey
from sqlalchemy.orm import relationship

propiedad_renta = Table(
    "propiedad_renta",
    Base.metadata,
    Column("propiedad_id", ForeignKey("propiedad.id", ondelete="CASCADE"), primary_key=True),
    Column("renta_id", ForeignKey("renta.id", ondelete="CASCADE"), primary_key=True)
)

class Renta(Base):
    __tablename__ = "renta"

    id = Column(Integer, primary_key=True, index=True)
    nombre_comercial = Column(String(255), nullable=False)
    razon_social = Column(String(255), nullable=False)
    renta_sin_iva = Column(Float, nullable=False)
    deposito_garantia_concepto = Column(String(255), nullable=True)
    deposito_garantia_monto = Column(Float, nullable=True)
    meses_gracia_concepto = Column(String(255), nullable=True)
    meses_gracia_fecha_inicio = Column(Date, nullable=True)
    meses_gracia_fecha_fin = Column(Date, nullable=True)
    renta_anticipada_concepto = Column(String(255), nullable=True)
    renta_anticipada_fecha_inicio = Column(Date, nullable=True)
    renta_anticipada_fecha_fin = Column(Date, nullable=True)
    renta_anticipada_renta_sin_iva = Column(Float, nullable=True)
    incremento_mes = Column(String(255), nullable=False)
    incremento_nota = Column(String(255), nullable=True)
    inicio_vigencia = Column(Date, nullable=False)
    fin_vigencia_forzosa = Column(Date, nullable=False)
    fin_vigencia_no_forzosa = Column(Date, nullable=True)
    vigencia_nota = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    propiedades = relationship("Propiedad", secondary=propiedad_renta, back_populates="rentas")