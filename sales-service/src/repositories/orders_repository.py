from flask import current_app as app

from api_messages.api_errors import InternalServerError
from database import db

import os
import uuid


class OrdersRepository:

  def __init__(self):
    pass
