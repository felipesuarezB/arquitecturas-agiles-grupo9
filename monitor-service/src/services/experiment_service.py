import uuid
from datetime import datetime, timedelta

from models.experimento import Experimento, EstadoExperimento, ExperimentoJsonSchema
from models.experimento import Caso, EstadoCaso, CasoJsonSchema
from models.experimento import ExperimentoConsultaJsonSchema
from api_messages.api_experiments import ExperimentCreated, ExperimentsList, ExperimentFound, ExperimentNotFound
from api_messages.api_experiments import CaseCreated, CaseNotFound, CaseUpdated, ExperimentUpdated
from api_messages.api_errors import InternalServerError, InvalidUrlPathParams
from database import db


class ExperimentService:

  def __init__(self):
    pass

  def create_experiment(self, new_experiment):
    new_experiment_data = Experimento(numero_casos=new_experiment['numero_casos'],
                                      max_reintentos=new_experiment['max_reintentos'],
                                      max_tiempo_espera_seg=new_experiment['max_tiempo_espera_seg'],
                                      estado=EstadoExperimento.PROGRAMADO.value)

    try:
      db.session.add(new_experiment_data)
      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return ExperimentCreated(new_experiment_data.id)

  def list_experiments(self, experiment_states=None):
    found_experiments = []
    try:
      query = db.session.query(Experimento)

      if experiment_states != None:
        filter_expr = Experimento.estado.in_(experiment_states)
        query = query.filter(filter_expr)

      found_experiments = query.all()
    except Exception as ex:
      raise InternalServerError() from ex

    found_experiments_json = [ExperimentoJsonSchema().dump(experiment) for experiment in found_experiments]

    return ExperimentsList(found_experiments_json)

  def get_experiment(self, id):
    path_id_uuid = None
    try:
      path_id_uuid = uuid.UUID(id)
    except Exception as ex:
      raise InvalidUrlPathParams() from ex

    found_experiment = None
    try:
      found_experiment = db.session.query(Experimento).filter(Experimento.id == path_id_uuid).first()
    except Exception as ex:
      raise InternalServerError() from ex

    if found_experiment is None:
      raise ExperimentNotFound()

    found_experiment_json = ExperimentoJsonSchema().dump(found_experiment)

    found_cases = []
    try:
      found_cases = db.session.query(Caso).filter(Caso.id_experimento == path_id_uuid).all()
    except Exception as ex:
      raise InternalServerError() from ex

    found_cases_json = [CasoJsonSchema().dump(case) for case in found_cases]

    found_experiment_view = {
        'experimento': found_experiment_json,
        'casos': found_cases_json
    }
    found_experiment_view_json = ExperimentoConsultaJsonSchema().dump(found_experiment_view)

    return ExperimentFound(found_experiment_view_json)

  def create_case(self, new_case):
    experiment_id_uuid = None
    try:
      experiment_id_uuid = uuid.UUID(new_case['id_experimento'])
    except Exception as ex:
      raise InvalidUrlPathParams() from ex

    new_case_data = Caso(id_experimento=experiment_id_uuid,
                         estado=EstadoCaso.EN_PROGRESO.value,
                         intentos=new_case['intentos'],
                         exitosos=new_case['exitosos'],
                         timeouts=new_case['timeouts'],
                         fallidos=new_case['fallidos'],
                         fecha_inicio=new_case['fecha_inicio'])

    try:
      db.session.add(new_case_data)
      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return CaseCreated(new_case_data.id)

  def update_case(self, id, updated_case):
    case_id_uuid = None
    try:
      case_id_uuid = uuid.UUID(id)
    except Exception as ex:
      raise InvalidUrlPathParams() from ex

    found_case = None
    try:
      found_case = db.session.query(Caso).filter(Caso.id == case_id_uuid).first()
    except Exception as ex:
      raise InternalServerError() from ex

    if found_case is None:
      raise CaseNotFound()

    try:
      if 'estado' in updated_case:
        found_case.estado = updated_case['estado']
      if 'intentos' in updated_case:
        found_case.intentos = updated_case['intentos']
      if 'exitosos' in updated_case:
        found_case.exitosos = updated_case['exitosos']
      if 'timeouts' in updated_case:
        found_case.timeouts = updated_case['timeouts']
      if 'fallidos' in updated_case:
        found_case.fallidos = updated_case['fallidos']
      if 'fecha_fin' in updated_case:
        found_case.fecha_fin = updated_case['fecha_fin']
      if 'duracion_deteccion' in updated_case:
        found_case.duracion_deteccion = updated_case['duracion_deteccion']

      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return CaseUpdated()

  def update_experiment(self, id, experiment_state):
    experiment_id_uuid = None
    try:
      experiment_id_uuid = uuid.UUID(id)
    except Exception as ex:
      raise InvalidUrlPathParams() from ex

    found_experiment = None
    try:
      found_experiment = db.session.query(Experimento).filter(Experimento.id == experiment_id_uuid).first()
    except Exception as ex:
      raise InternalServerError() from ex

    if found_experiment is None:
      raise ExperimentNotFound()

    try:
      found_experiment.estado = experiment_state

      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return ExperimentUpdated()


experiment_service = ExperimentService()
