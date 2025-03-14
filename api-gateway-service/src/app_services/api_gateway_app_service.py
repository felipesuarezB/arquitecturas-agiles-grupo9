from flask import current_app as app

import os
import time
import uuid
import random
import requests
from datetime import datetime

from api_messages.api_errors import InternalServerError, TokenInvalidOrExpired


class ApiGatewayAppService:

  def __init__(self):
    auth_service_url = os.environ.get('AUTH_SERVICE_URL', 'http://localhost:8084')
    sales_service_url = os.environ.get('SALES_SERVICE_URL', 'http://localhost:8081')
    self.urls = {
        'ventas_clientes': f"{sales_service_url}/ventas/clientes",
        'ventas_ordenes': f"{sales_service_url}/ventas/ordenes",
        'ventas_logs': f"{sales_service_url}/ventas/ordenes/logs",
        'auth_generar_token': f"{auth_service_url}/auth/generar_token",
        'auth_validar_token': f"{auth_service_url}/auth/validar_token"
    }

    client_timeout = os.environ.get('CLIENT_TIMEOUT', 5)
    self.client_timeout = int(client_timeout)

  def send_request_auth_generate_token(self, auth_req):
    try:
      app.logger.debug(f"auth_generate_token - Enviando petición a {self.urls['auth_generar_token']}")

      response = requests.post(self.urls['auth_generar_token'], json=auth_req, timeout=self.client_timeout)
      app.logger.debug(f"auth_generate_token {self.urls['auth_generar_token']} - Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      raise InternalServerError from ex

    res_data = response.json()
    code = response.status_code

    return res_data, code

  def send_request_sales_customers(self, auth_header):
    authenticated = self._send_request_auth_validate_token(auth_header)

    if not authenticated:
      raise TokenInvalidOrExpired()

    headers = {
        'Authorization': auth_header
    }

    try:
      app.logger.debug(f"sales_customers - Enviando petición a {self.urls['ventas_clientes']}")

      response = requests.get(self.urls['ventas_clientes'], headers=headers, timeout=self.client_timeout)
      app.logger.debug(f"sales_customers {self.urls['ventas_clientes']} - Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      raise InternalServerError from ex

    res_data = response.json()
    code = response.status_code

    return res_data, code

  def send_request_sales_orders(self, orders_req, auth_header):
    authenticated = self._send_request_auth_validate_token(auth_header)

    if not authenticated:
      raise TokenInvalidOrExpired()

    headers = {
        'Authorization': auth_header
    }

    try:
      app.logger.debug(f"sales_orders - Enviando petición a {self.urls['ventas_ordenes']}")

      response = requests.post(self.urls['ventas_ordenes'], json=orders_req, headers=headers, timeout=self.client_timeout)
      app.logger.debug(f"sales_orders {self.urls['ventas_ordenes']} - Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      raise InternalServerError from ex

    res_data = response.json()
    code = response.status_code

    return res_data, code

  def send_request_sales_logs(self, id, auth_header):
    authenticated = self._send_request_auth_validate_token(auth_header)

    if not authenticated:
      raise TokenInvalidOrExpired()

    headers = {
        'Authorization': auth_header
    }

    try:
      target_url = f"{self.urls['ventas_logs']}/{id}"
      app.logger.debug(f"sales_logs - Enviando petición a {target_url}")

      response = requests.get(target_url, headers=headers, timeout=self.client_timeout)
      app.logger.debug(f"sales_logs {target_url} - Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      raise InternalServerError from ex

    res_data = response.json()
    code = response.status_code

    return res_data, code

  def _send_request_auth_validate_token(self, auth_header):
    authenticated = False

    headers = {
        'Authorization': auth_header
    }

    try:
      app.logger.debug(f"auth_validate_token - Enviando petición a {self.urls['auth_validar_token']}")

      response = requests.get(self.urls['auth_validar_token'], headers=headers, timeout=self.client_timeout)
      app.logger.debug(f"auth_validate_token {self.urls['auth_validar_token']} - Status Code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as ex:
      raise InternalServerError from ex

    if response.status_code == 200:
      authenticated = True
    else:
      authenticated = False

    res_data = response.json()
    code = response.status_code

    return authenticated
