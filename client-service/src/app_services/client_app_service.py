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
        'customers': f"{api_gateway_url}/ventas/clientes",
        'orders': f"{api_gateway_url}/ventas/ordenes",
        'authenticate': f"{api_gateway_url}/auth/generar_token"
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
                autenticaciones_exitosas=0,
                autenticaciones_fallidas=0,
                autorizaciones_exitosas=0,
                autorizaciones_fallidas=0,
                fecha_inicio=datetime.today())
    experiments_repository.create_case(case)

    app.logger.debug(f"Caso {case.id} EN PROGRESO!")

    start_time = time.time()

    for num_attempt in range(1, experiment.max_intentos+1):
      app.logger.debug(f"Caso {case.id} Intento {num_attempt}")
      self._request_attempt(case, num_attempt)

    end_time = time.time()
    duration = end_time - start_time

    case.fecha_fin = datetime.today()
    case.duracion_segundos = duration
    case.estado = EstadoCaso.FINALIZADO.value

    experiments_repository.update_case(case)
    app.logger.debug(f"Caso {case.id} FINALIZADO!")

  def _request_attempt(self, case: Caso, num_attempt: int):
    case.intentos = num_attempt

    _, token = self._request_authentication_attempt(case, num_attempt)
    self._request_authorization_attempt(case, num_attempt, token)

    experiments_repository.update_case(case)

  def _request_authentication_attempt(self, case: Caso, num_attempt: int):
    authenticated = False
    token = ""

    credentials_data = self._get_random_credentials_data()

    try:
      app.logger.debug(f"Caso {case.id} - {num_attempt} Enviando petición a {self.urls['authenticate']}")
      response = requests.post(self.urls['authenticate'], json=credentials_data, timeout=self.client_timeout)
      app.logger.debug(f"Caso {case.id} {self.urls['authenticate']} - {num_attempt} Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      case.autenticaciones_timeouts += 1
      return authenticated, token

    if response.status_code == 200:
      case.autenticaciones_exitosas += 1
      authenticated = True
      res_json = response.json()
      token = res_json['token']
    else:
      case.autenticaciones_fallidas += 1
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

  def _request_authorization_attempt(self, case: Caso, num_attempt: int, token: str):
    success = False
    headers = {
        'Authorization': f"Bearer {token}"
    }
    target_url = ""
    if case.tipo_caso == TipoCaso.CLIENTES.value:
      target_url = self.urls['customers']
    elif case.tipo_caso == TipoCaso.ORDENES.value:
      target_url = self.urls['orders']

    try:
      app.logger.debug(f"Caso {case.id} - {num_attempt} Enviando petición a {target_url}")

      response = None
      if case.tipo_caso == TipoCaso.CLIENTES.value:
        response = requests.get(target_url, headers=headers, timeout=self.client_timeout)
      elif case.tipo_caso == TipoCaso.ORDENES.value:
        response = requests.post(target_url, headers=headers, timeout=self.client_timeout)

      app.logger.debug(f"Caso {case.id} {target_url} - {num_attempt} Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      case.autorizaciones_timeouts += 1
      return success

    if response.status_code == 200:
      case.autorizaciones_exitosas += 1
      success = True
    else:
      case.autorizaciones_fallidas += 1
      success = False

    return success
