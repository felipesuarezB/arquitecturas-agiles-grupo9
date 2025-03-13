from flask import current_app as app

from api_messages.api_errors import InternalServerError
from models.orders import Order, OrderEventLog
from database import db

import os
import uuid
import datetime


class OrdersRepository:

  def __init__(self):
    pass

  def create_order(self, date, product, value):
    new_order = Order(uuid.uuid4(), date, product, value)
    return new_order

  def create_order_log(self, order_id):
    new_log = OrderEventLog(
      id_tabla=uuid.uuid4(),
      id_order=order_id,
      date_log=datetime.datetime.now()
    )
    return new_log

  def get_order_logs(self):
    # En un entorno real, aquí se haría una consulta a la base de datos
    # Por ahora, devolvemos algunos datos simulados para fines de demostración
    logs = [
      OrderEventLog(
        id_tabla=uuid.uuid4(),
        id_order=uuid.uuid4(),
        date_log=datetime.datetime.now()
      ),
      OrderEventLog(
        id_tabla=uuid.uuid4(),
        id_order=uuid.uuid4(),
        date_log=datetime.datetime.now() - datetime.timedelta(hours=1)
      )
    ]
    return logs
