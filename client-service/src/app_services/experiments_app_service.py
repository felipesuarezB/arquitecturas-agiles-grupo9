from flask import current_app as app

import uuid

from models.experimento import Experimento, EstadoExperimento, ExperimentoJsonSchema, ExperimentoConsultaJsonSchema
from models.experimento import Caso, EstadoCaso, CasoJsonSchema
from api_messages.api_errors import InvalidUrlPathParams
from api_messages.api_experiments import ExperimentCreated, ExperimentsList, ExperimentNotFound, ExperimentFound
from api_messages.api_experiments import CaseCreated, CaseNotFound, CaseUpdated, ExperimentUpdated

from repositories import experiments_repository


class ExperimentsAppService:

  def __init__(self):
    pass

  def create_experiment(self, new_experiment_req: ExperimentoJsonSchema):
    experiment = Experimento(tipo_caso=new_experiment_req['tipo_caso'],
                             numero_casos=new_experiment_req['numero_casos'],
                             max_intentos=new_experiment_req['max_intentos'],
                             estado=EstadoExperimento.PROGRAMADO.value)

    experiments_repository.create_experiment(experiment)

    return ExperimentCreated(experiment.id)

  def list_experiments(self):
    found_experiments = experiments_repository.find_experiments()
    found_experiments_json = [ExperimentoJsonSchema().dump(experiment) for experiment in found_experiments]

    return ExperimentsList(found_experiments_json)

  def get_experiment(self, experiment_id: str):
    experiment_id_uuid = None
    try:
      experiment_id_uuid = uuid.UUID(experiment_id)
    except Exception as ex:
      raise InvalidUrlPathParams() from ex

    found_experiment = experiments_repository.find_experiment_by_id(experiment_id_uuid)

    if found_experiment is None:
      raise ExperimentNotFound()

    found_cases = experiments_repository.find_cases_by_experiment_id(found_experiment.id)

    found_experiment_response = {
        'experimento': found_experiment,
        'casos': found_cases
    }
    found_experiment_response_json = ExperimentoConsultaJsonSchema().dump(found_experiment_response)

    return ExperimentFound(found_experiment_response_json)

  def create_case(self, new_case_req: CasoJsonSchema):
    experiment_id_uuid = None
    try:
      experiment_id_uuid = uuid.UUID(new_case_req['id_experimento'])
    except Exception as ex:
      raise InvalidUrlPathParams() from ex

    case = Caso(id_experimento=experiment_id_uuid,
                tipo_caso=new_case_req['tipo_caso'],
                estado=EstadoCaso.EN_PROGRESO.value,
                intentos=new_case_req['intentos'],
                autenticaciones_exitosas=new_case_req['autenticaciones_exitosas'],
                autenticaciones_fallidas=new_case_req['autenticaciones_fallidas'],
                autorizaciones_exitosas=new_case_req['autorizaciones_exitosas'],
                autorizaciones_fallidas=new_case_req['autorizaciones_fallidas'],
                fecha_inicio=new_case_req['fecha_inicio'])

    experiments_repository.create_case(case)

    return CaseCreated(case.id)

  def update_case(self, case_id: str, updated_case_req: CasoJsonSchema):
    case_id_uuid = None
    try:
      case_id_uuid = uuid.UUID(case_id)
    except Exception as ex:
      raise InvalidUrlPathParams() from ex

    found_case = experiments_repository.find_case_by_id(case_id_uuid)

    if found_case is None:
      raise CaseNotFound()

    experiments_repository.update_case(found_case, updated_case_req)

    return CaseUpdated()

  def update_experiment(self, experiment_id: str, new_experiment_state: int):
    experiment_id_uuid = None
    try:
      experiment_id_uuid = uuid.UUID(experiment_id)
    except Exception as ex:
      raise InvalidUrlPathParams() from ex

    found_experiment = experiments_repository.find_experiment_by_id(experiment_id_uuid)

    if found_experiment is None:
      raise ExperimentNotFound()

    experiments_repository.update_experiment_state(found_experiment, new_experiment_state)

    return ExperimentUpdated()
