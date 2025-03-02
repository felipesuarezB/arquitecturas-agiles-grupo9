from api_messages.base_api_error import ApiError


class ExperimentCreated:
  code = 201

  def __init__(self, experiment_id):
    self.message = "Experimento creado exitosamente."
    self.experiment_id = experiment_id


class ExperimentsList:
  code = 200

  def __init__(self, found_experiments):
    self.experiments = found_experiments


class ExperimentFound:
  code = 200

  def __init__(self, found_experiment_view):
    self.experiment_view = found_experiment_view


class ExperimentNotFound(ApiError):
  code = 404

  def __init__(self):
    self.message = "Experimento no encontrado."


class CaseCreated:
  code = 201

  def __init__(self, case_id):
    self.message = "Caso creado exitosamente."
    self.case_id = case_id


class CaseNotFound(ApiError):
  code = 404

  def __init__(self):
    self.message = "Caso no encontrado."


class CaseUpdated:
  code = 200

  def __init__(self):
    self.message = "Caso actualizado exitosamente."


class ExperimentUpdated:
  code = 200

  def __init__(self):
    self.message = "Experimento actualizado exitosamente."
