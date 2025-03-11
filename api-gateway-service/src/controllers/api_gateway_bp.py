from flask import request, current_app
from flask import jsonify, make_response
from flask.views import MethodView
from flask_smorest import Blueprint

from app_services import api_gateway_app_service

api_gateway_bp = Blueprint('api_gateway', __name__, url_prefix='/', description="API Gateway Endpoints.")


@api_gateway_bp.route("/auth/generar_token", methods=["POST"])
def auth_generate_token():
  auth_req = request.get_json()
  res_data, code = api_gateway_app_service.send_request_auth_generate_token(auth_req)
  res = jsonify(res_data)

  return res, code


@api_gateway_bp.route("/ventas/clientes", methods=["GET"])
def sales_clients():
  auth_header = request.headers['Authorization']
  res_data, code = api_gateway_app_service.send_request_sales_clients(auth_header)
  res = jsonify(res_data)

  return res, code


@api_gateway_bp.route("/ventas/ordenes", methods=["POST"])
def sales_orders():
  orders_req = request.get_json()
  auth_header = request.headers['Authorization']
  res_data, code = api_gateway_app_service.send_request_sales_orders(orders_req, auth_header)
  res = jsonify(res_data)

  return res, code
