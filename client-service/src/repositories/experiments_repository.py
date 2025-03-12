from flask import current_app as app

import uuid

from models.experimento import Experimento, EstadoExperimento
from models.experimento import Caso, EstadoCaso
from api_messages.api_errors import InternalServerError

from database import db


class ExperimentsRepository:

  def __init__(self):
    pass

  def create_experiment(self, new_experiment: Experimento):
    try:
      db.session.add(new_experiment)
      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return new_experiment.id

  def find_experiments(self, experiment_states: list[EstadoExperimento] = None):
    found_experiments = []
    try:
      query = db.session.query(Experimento)

      if experiment_states != None:
        experiment_states = [s.value for s in experiment_states]
        filter_expr = Experimento.estado.in_(experiment_states)
        query = query.filter(filter_expr)

      found_experiments = query.all()
    except Exception as ex:
      raise InternalServerError() from ex

    return found_experiments

  def find_experiment_by_id(self, experiment_id_uuid: uuid.UUID):
    found_experiment = None
    try:
      filter_expr = Experimento.id == experiment_id_uuid
      found_experiment = db.session.query(Experimento).filter(filter_expr).first()
    except Exception as ex:
      raise InternalServerError() from ex

    return found_experiment

  def find_cases_by_experiment_id(self, experiment_id_uuid: uuid.UUID):
    found_cases = []
    try:
      filter_expr = Caso.id_experimento == experiment_id_uuid
      found_cases = db.session.query(Caso).filter(filter_expr).all()
    except Exception as ex:
      raise InternalServerError() from ex

    return found_cases

  def create_case(self, new_case: Caso):
    try:
      db.session.add(new_case)
      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return new_case.id

  def find_case_by_id(self, case_id_uuid: uuid.UUID):
    found_case = None
    try:
      found_case = db.session.query(Caso).filter(Caso.id == case_id_uuid).first()
    except Exception as ex:
      raise InternalServerError() from ex

    return found_case

  def update_case(self, case: Caso):
    try:
      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return case.id

  def update_experiment_state(self, experiment: Experimento, new_experiment_state: EstadoExperimento):
    try:
      experiment.estado = new_experiment_state.value

      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return experiment.id
