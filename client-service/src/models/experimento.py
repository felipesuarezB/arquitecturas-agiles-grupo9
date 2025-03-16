from sqlalchemy import Column, String, Integer, DateTime, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from enum import Enum
import uuid
from datetime import datetime

from database import db


class Experimento(db.Model):
  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
  tipo_caso = Column(Integer, nullable=False, default=1)
  numero_casos = Column(Integer, nullable=False, default=1)
  max_intentos = Column(Integer, nullable=False, default=3)
  estado = Column(Integer, nullable=False, default=1)


class EstadoExperimento(Enum):
  PROGRAMADO = 1
  EN_PROGRESO = 2
  FINALIZADO = 3


class TipoCaso(Enum):
  CLIENTES = 1
  ORDENES = 2


class ExperimentoJsonSchema(Schema):
  id = fields.String(attribute='id')
  tipo_caso = fields.Integer(attribute='tipo_caso')
  numero_casos = fields.Integer(attribute='numero_casos')
  max_intentos = fields.Integer(attribute='max_intentos')
  estado = fields.Integer(attribute='estado')


class Caso(db.Model):
  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
  id_experimento = Column(UUID(as_uuid=True), ForeignKey('experimento.id'), nullable=False)
  numero = Column(Integer, nullable=False, default=1)
  tipo_caso = Column(Integer, nullable=False, default=1)
  estado = Column(Integer, nullable=False, default=1)
  intentos = Column(Integer, nullable=False, default=0)
  peticion_auth_exitosas = Column(Integer, nullable=False, default=0)
  peticion_auth_fallidas = Column(Integer, nullable=False, default=0)
  peticion_auth_timeouts = Column(Integer, nullable=False, default=0)
  peticion_clientes_exitosas = Column(Integer, nullable=False, default=0)
  peticion_clientes_fallidas = Column(Integer, nullable=False, default=0)
  peticion_clientes_timeouts = Column(Integer, nullable=False, default=0)
  peticion_ordenes_exitosas = Column(Integer, nullable=False, default=0)
  peticion_ordenes_fallidas = Column(Integer, nullable=False, default=0)
  peticion_ordenes_timeouts = Column(Integer, nullable=False, default=0)
  peticion_logs_exitosas = Column(Integer, nullable=False, default=0)
  peticion_logs_fallidas = Column(Integer, nullable=False, default=0)
  peticion_logs_timeouts = Column(Integer, nullable=False, default=0)
  fecha_inicio = Column(DateTime, nullable=False, default=datetime.today())
  fecha_fin = Column(DateTime)
  duracion_segundos = Column(Integer)


class EstadoCaso(Enum):
  EN_PROGRESO = 1
  FINALIZADO = 2


class CasoJsonSchema(Schema):
  id = fields.String(attribute='id')
  id_experimento = fields.String(attribute='id_experimento')
  numero = fields.Integer(attribute='numero')
  tipo_caso = fields.Integer(attribute='tipo_caso')
  estado = fields.Integer(attribute='estado')
  intentos = fields.Integer(attribute='intentos')
  peticion_auth_exitosas = fields.Integer(attribute='peticion_auth_exitosas')
  peticion_auth_fallidas = fields.Integer(attribute='peticion_auth_fallidas')
  peticion_auth_timeouts = fields.Integer(attribute='peticion_auth_timeouts')
  peticion_clientes_exitosas = fields.Integer(attribute='peticion_clientes_exitosas')
  peticion_clientes_fallidas = fields.Integer(attribute='peticion_clientes_fallidas')
  peticion_clientes_timeouts = fields.Integer(attribute='peticion_clientes_timeouts')
  peticion_ordenes_exitosas = fields.Integer(attribute='peticion_ordenes_exitosas')
  peticion_ordenes_fallidas = fields.Integer(attribute='peticion_ordenes_fallidas')
  peticion_ordenes_timeouts = fields.Integer(attribute='peticion_ordenes_timeouts')
  peticion_logs_exitosas = fields.Integer(attribute='peticion_logs_exitosas')
  peticion_logs_fallidas = fields.Integer(attribute='peticion_logs_fallidas')
  peticion_logs_timeouts = fields.Integer(attribute='peticion_logs_timeouts')
  fecha_inicio = fields.String(attribute='fecha_inicio')
  fecha_fin = fields.String(attribute='fecha_fin')
  duracion_segundos = fields.String(attribute='duracion_segundos')


class ExperimentoConsultaJsonSchema(Schema):
  experimento = fields.Nested(ExperimentoJsonSchema)
  casos = fields.List(fields.Nested(CasoJsonSchema))
