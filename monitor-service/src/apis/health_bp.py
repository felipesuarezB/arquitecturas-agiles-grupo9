from flask import request, current_app
from flask import jsonify
from flask_smorest import Blueprint

from datetime import datetime

health_bp = Blueprint(name='health', import_name=__name__, url_prefix='/health', description="API de Health Check.")


@health_bp.route('/ping', methods=['GET'])
def ping_posts():
  response = {
      'status': 'UP',
      'componentName': 'monitor-service',
      'currentTime': datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  }

  return response, 200
