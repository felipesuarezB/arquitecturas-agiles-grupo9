from flask import jsonify
from flask_smorest import Blueprint

from app_services import sales_app_service
from models.orders import NewOrderCommandJson


ventas_bp = Blueprint(name='ventas', import_name=__name__, url_prefix='/ventas', description="API de Ventas.")


@ventas_bp.route('/clientes', methods=['GET'])
def list_customers():
  result = sales_app_service.list_customers()
  res = jsonify(result.__dict__)

  return res, result.code


@ventas_bp.route('/ordenes', methods=['POST'])
@ventas_bp.arguments(NewOrderCommandJson)
def create_order(new_order_cmd):
  result = sales_app_service.create_order(new_order_cmd)
  res = jsonify(result.__dict__)

  return res, result.code
