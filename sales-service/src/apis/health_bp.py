from flask import jsonify
from flask_smorest import Blueprint
from services.health_service import health_service


health_bp = Blueprint(name='health', import_name=__name__, url_prefix='/health', description="API de Health Check.")


@health_bp.route('/ping', methods=['GET'])
def ping():
  result = health_service.get_health_check()
  res_json = jsonify(result.__dict__)

  return res_json, result.code
