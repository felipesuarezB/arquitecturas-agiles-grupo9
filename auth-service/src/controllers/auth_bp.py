from flask import request, current_app
from flask import jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from app_services import auth_app_service
from models.authentication import UserCredentialsJson, UserToken

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', description="API de Autenticación.")


@auth_bp.route("/generar_token", methods=["POST"])
@auth_bp.arguments(UserCredentialsJson)
def auth_generate_token(user_creds):
  result = auth_app_service.authenticate_user(user_creds)
  res = jsonify(result.__dict__)

  return res, result.code


@auth_bp.route("/validar_token", methods=["POST"])
@jwt_required()
def auth_generate_token():
  jwt_payload = get_jwt()
  user_token = UserToken(jwt_payload['sub'], jwt_payload['user_role'])

  result = auth_app_service.validate_token(user_token)
  res = jsonify(result.__dict__)

  return res, result.code
