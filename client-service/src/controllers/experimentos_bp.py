from flask import request, current_app
from flask import jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint

from app_services import experiments_app_service
from models.experimento import ExperimentoJsonSchema, ExperimentoConsultaJsonSchema

experimentos_bp = Blueprint('experimentos', __name__, url_prefix='/experimentos', description="API de Experimentos.")


@experimentos_bp.route("", methods=["POST"])
@experimentos_bp.arguments(ExperimentoJsonSchema)
def create_experiment(new_experiment_req):
  result = experiments_app_service.create_experiment(new_experiment_req)
  res = jsonify(result.__dict__)

  return res, result.code


@experimentos_bp.route("", methods=["GET"])
@experimentos_bp.response(200, ExperimentoJsonSchema)
def list_exercises():
  result = experiments_app_service.list_experiments()
  res = jsonify(result.experiments)

  return res, result.code


@experimentos_bp.route("/<string:id>")
class ExperimentosResource(MethodView):

  @experimentos_bp.response(200, ExperimentoConsultaJsonSchema)
  def get(self, id):
    result = experiments_app_service.get_experiment(id)
    res = jsonify(result.experiment_view)

    return res, result.code
