from flask import request, current_app, make_response
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from datetime import datetime, timedelta

from services.experiment_service import experiment_service
from models.experimento import ExperimentoJsonSchema, ExperimentoConsultaJsonSchema

experimentos_bp = Blueprint('experimentos', __name__, url_prefix='/experimentos', description="API de Experimentos.")


@experimentos_bp.route("", methods=["POST"])
@experimentos_bp.arguments(ExperimentoJsonSchema)
def create_experiment(new_experiment):
  result = experiment_service.create_experiment(new_experiment)
  res_json = jsonify(result.__dict__)

  return res_json, result.code


@experimentos_bp.route("", methods=["GET"])
def list_exercises():
  result = experiment_service.list_experiments()
  res_json = jsonify(result.experiments)

  return res_json, result.code


@experimentos_bp.route("/<string:id>")
class ExperimentosResource(MethodView):

  @experimentos_bp.response(200, ExperimentoConsultaJsonSchema)
  def get(self, id):
    result = experiment_service.get_experiment(id)
    res_json = jsonify(result.experiment_view)

    return res_json, result.code
