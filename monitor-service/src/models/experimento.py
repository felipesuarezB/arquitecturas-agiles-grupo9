from sqlalchemy import Column, String, Integer, DateTime, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

import uuid
from datetime import datetime
from enum import Enum

from database import db


class Experimento(db.Model):
  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
  numero_casos = Column(Integer, nullable=False)
  max_reintentos = Column(Integer, nullable=False)
  max_tiempo_espera_seg = Column(Integer, nullable=False)
  estado = Column(Integer, nullable=False)


class EstadoExperimento(Enum):
  PROGRAMADO = 1
  EN_PROGRESO = 2
  FINALIZADO = 3


class ExperimentoJsonSchema(Schema):
  id = fields.String(attribute='id')
  numero_casos = fields.Integer(attribute='numero_casos')
  max_reintentos = fields.Integer(attribute='max_reintentos')
  max_tiempo_espera_seg = fields.Integer(attribute='max_tiempo_espera_seg')
  estado = fields.Integer(attribute='estado')


class Caso(db.Model):
  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
  id_experimento = Column(UUID(as_uuid=True), ForeignKey('experimento.id'), nullable=False)
  estado = Column(Integer, nullable=False)
  intentos = Column(Integer, nullable=False, default=0)
  exitosos = Column(Integer, nullable=False, default=0)
  timeouts = Column(Integer, nullable=False, default=0)
  fallidos = Column(Integer, nullable=False, default=0)
  fecha_inicio = Column(DateTime, nullable=False)
  fecha_fin = Column(DateTime)
  duracion_deteccion = Column(Integer)


class EstadoCaso(Enum):
  EN_PROGRESO = 1
  FINALIZADO = 2


class CasoJsonSchema(Schema):
  id = fields.String(attribute='id')
  id_experimento = fields.String(attribute='id_experimento')
  estado = fields.Integer(attribute='estado')
  intentos = fields.Integer(attribute='intentos')
  exitosos = fields.Integer(attribute='exitosos')
  timeouts = fields.Integer(attribute='timeouts')
  fallidos = fields.Integer(attribute='fallidos')
  fecha_inicio = fields.String(attribute='fecha_inicio')
  fecha_fin = fields.String(attribute='fecha_fin')
  duracion_deteccion = fields.String(attribute='duracion_deteccion')


class ExperimentoConsultaJsonSchema(Schema):
  experimento = fields.Nested(ExperimentoJsonSchema)
  casos = fields.List(fields.Nested(CasoJsonSchema))
