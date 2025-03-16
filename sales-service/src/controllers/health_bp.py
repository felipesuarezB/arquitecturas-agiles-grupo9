from flask import jsonify
from flask_smorest import Blueprint
from app_services import health_app_service


health_bp = Blueprint(name='health', import_name=__name__, url_prefix='/health', description="API de Health Check.")


@health_bp.route('/ping', methods=['GET'])
def ping():
  result = health_app_service.get_health_check()
  res = jsonify(result.__dict__)

  return res, result.code
