from flask import current_app as app

import os
import time
import uuid
import random
import requests
from datetime import datetime

from models.experimento import Experimento, EstadoExperimento
from models.experimento import Caso, TipoCaso, EstadoCaso
from api_messages.api_errors import InternalServerError

from repositories import experiments_repository


class ClientAppService:

  def __init__(self):
    api_gateway_url = os.environ.get('API_GATEWAY_URL', 'http://localhost:8083')
    self.urls = {
        'authenticate': f"{api_gateway_url}/auth/generar_token",
        'customers': f"{api_gateway_url}/ventas/clientes",
        'orders': f"{api_gateway_url}/ventas/ordenes",
        'logs': f"{api_gateway_url}/ventas/ordenes/logs",
    }

    client_timeout = os.environ.get('CLIENT_TIMEOUT', 5)
    self.client_timeout = int(client_timeout)

    self.credentials_username = os.environ.get('CREDENTIALS_USERNAME', '')
    self.credentials_password = os.environ.get('CREDENTIALS_PASSWORD', '')

  def simulate_client_requests(self):
    experiments = experiments_repository.find_experiments([EstadoExperimento.PROGRAMADO])

    for experiment in experiments:
      experiments_repository.update_experiment_state(experiment, EstadoExperimento.EN_PROGRESO)
      app.logger.debug(f"Experimento {experiment.id} EN PROGRESO!")

      for num_case in range(experiment.numero_casos):
        self._process_case(experiment, num_case+1)

      experiments_repository.update_experiment_state(experiment, EstadoExperimento.FINALIZADO)
      app.logger.debug(f"Experimento {experiment.id} FINALIZADO!")

  def _process_case(self, experiment: Experimento, num_case: int):
    case = Caso(id_experimento=experiment.id,
                numero=num_case,
                tipo_caso=experiment.tipo_caso,
                intentos=0,
                fecha_inicio=datetime.today())
    experiments_repository.create_case(case)

    app.logger.debug(f"Caso {case.id} EN PROGRESO!")

    start_time = time.time()

    for num_attempt in range(1, experiment.max_intentos+1):
      app.logger.debug(f"Caso {case.id} Intento {num_attempt}")
      if experiment.tipo_caso == TipoCaso.CLIENTES.value:
        self._request_attempt_case_1(case, num_attempt)
      elif experiment.tipo_caso == TipoCaso.ORDENES.value:
        self._request_attempt_case_2(case, num_attempt)

    end_time = time.time()
    duration = end_time - start_time

    case.fecha_fin = datetime.today()
    case.duracion_segundos = duration
    case.estado = EstadoCaso.FINALIZADO.value

    experiments_repository.update_case(case)
    app.logger.debug(f"Caso {case.id} FINALIZADO!")

  def _request_attempt_case_1(self, case: Caso, num_attempt: int):
    case.intentos = num_attempt

    _, token = self._send_auth_request(case, num_attempt)
    self._send_customers_request(case, num_attempt, token)

    experiments_repository.update_case(case)

  def _send_auth_request(self, case: Caso, num_attempt: int):
    authenticated = False
    token = ""

    credentials_data = self._get_random_credentials_data()

    try:
      app.logger.debug(f"Caso {case.id} - {num_attempt} Enviando petición a {self.urls['authenticate']}")
      response = requests.post(self.urls['authenticate'], json=credentials_data, timeout=self.client_timeout)
      app.logger.debug(f"Caso {case.id} {self.urls['authenticate']} - {num_attempt} Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      case.peticion_auth_timeouts += 1
      return authenticated, token

    if response.status_code == 200:
      case.peticion_auth_exitosas += 1
      authenticated = True
      res_json = response.json()
      token = res_json['token']
    else:
      case.peticion_auth_fallidas += 1
      authenticated = False
      token = ""

    return authenticated, token

  def _get_random_credentials_data(self):
    data = {}
    r = random.random()
    if r < 0.5:
      data = {
          'username': self.credentials_username,
          'password': self.credentials_password
      }
    else:
      data = {
          'username': self.credentials_username,
          'password': ''
      }

    return data

  def _send_customers_request(self, case: Caso, num_attempt: int, token: str):
    success = False
    headers = {
        'Authorization': f"Bearer {token}"
    }

    try:
      app.logger.debug(f"Caso {case.id} - {num_attempt} Enviando petición a {self.urls['customers']}")
      response = requests.get(self.urls['customers'], headers=headers, timeout=self.client_timeout)
      app.logger.debug(f"Caso {case.id} {self.urls['customers']} - {num_attempt} Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      case.peticion_clientes_timeouts += 1
      return success

    if response.status_code == 200:
      case.peticion_clientes_exitosas += 1
      success = True
    else:
      case.peticion_clientes_fallidas += 1
      success = False

    return success

  def _request_attempt_case_2(self, case: Caso, num_attempt: int):
    case.intentos = num_attempt

    _, token = self._send_auth_request(case, num_attempt)
    _, order_id = self._send_orders_request(case, num_attempt, token)
    _, self._send_logs_request(case, num_attempt, token, order_id)

    experiments_repository.update_case(case)

  def _send_orders_request(self, case: Caso, num_attempt: int, token: str):
    success = False
    order_id = ""

    headers = {
        'Authorization': f"Bearer {token}"
    }
    req = {
        "order_date": "2025-03-13T19:00:00",
        "product": 1,
        "value": 100
    }

    try:
      app.logger.debug(f"Caso {case.id} - {num_attempt} Enviando petición a {self.urls['orders']}")
      response = requests.post(self.urls['orders'], json=req, headers=headers, timeout=self.client_timeout)
      app.logger.debug(f"Caso {case.id} {self.urls['orders']} - {num_attempt} Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      case.peticion_ordenes_timeouts += 1
      return success, order_id

    if response.status_code == 200:
      case.peticion_ordenes_exitosas += 1
      success = True
      res_json = response.json()
      order_id = res_json['order_id']
    else:
      case.peticion_ordenes_fallidas += 1
      success = False

    return success, order_id

  def _send_logs_request(self, case: Caso, num_attempt: int, token: str, order_id: str):
    success = False

    headers = {
        'Authorization': f"Bearer {token}"
    }

    try:
      target_url = f"{self.urls['logs']}/{order_id}"
      app.logger.debug(f"Caso {case.id} - {num_attempt} Enviando petición a {target_url}")
      response = requests.get(target_url, headers=headers, timeout=self.client_timeout)
      app.logger.debug(f"Caso {case.id} {target_url} - {num_attempt} Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      case.peticion_logs_timeouts += 1
      return success

    if response.status_code == 200:
      case.peticion_logs_exitosas += 1
      success = True
    else:
      case.peticion_logs_fallidas += 1
      success = False

    return success
