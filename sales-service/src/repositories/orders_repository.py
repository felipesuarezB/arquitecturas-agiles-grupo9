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
    new_order = Order(id=uuid.uuid4(),
                      order_date=date,
                      product=product,
                      value=value)

    try:
      db.session.add(new_order)
      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return new_order

  def create_order_log(self, order_id):
    new_log = OrderEventLog(
        id=uuid.uuid4(),
        id_order=order_id,
        date_log=datetime.datetime.now())

    try:
      db.session.add(new_log)
      db.session.commit()
    except Exception as ex:
      db.session.rollback()
      raise InternalServerError() from ex

    return new_log

  def get_order_log(self, order_id):
    try:
      log = db.session.query(OrderEventLog).filter(OrderEventLog.id_order == order_id).first()
    except Exception as ex:
      raise InternalServerError() from ex

    return log
