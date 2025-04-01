from sqlalchemy.orm import Session
from app.models.auditoria import Auditoria
import json
from datetime import date, datetime

def get_all_auditorias(
    db: Session,
    operacion: str = None,
    tabla_afectada: str = None,
    usuario_username: str = None,
):
    query = db.query(Auditoria)

    if operacion:
        query = query.filter(Auditoria.operacion.ilike(f"%{operacion}%"))

    if tabla_afectada:
        query = query.filter(Auditoria.tabla_afectada.ilike(f"%{tabla_afectada}%"))

    if usuario_username:
        query = query.filter(Auditoria.usuario_username.ilike(f"%{usuario_username}%"))

    auditorias = query.all()

    for auditoria in auditorias:
        auditoria.valores_anteriores = json.loads(auditoria.valores_anteriores) if auditoria.valores_anteriores else None
        auditoria.valores_nuevos = json.loads(auditoria.valores_nuevos) if auditoria.valores_nuevos else None


    return auditorias

def serialize_dates(obj):
    """Convierte objetos datetime y date en strings antes de guardarlos en JSON."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def create_auditoria(db, operacion, tabla_afectada, registro_tabla_id, usuario_username, valores_anteriores, valores_nuevos):
    valores_nuevos_serializados = json.dumps(valores_nuevos, default=serialize_dates)
    valores_anteriores_serializados = json.dumps(valores_anteriores, default=serialize_dates) if valores_anteriores else None

    auditoria = Auditoria(
        operacion=operacion,
        tabla_afectada=tabla_afectada,
        registro_tabla_id=registro_tabla_id,
        usuario_username=usuario_username,
        valores_anteriores=valores_anteriores_serializados,
        valores_nuevos=valores_nuevos_serializados,
    )
    db.add(auditoria)
    db.commit()
    db.refresh(auditoria)
    return auditoria