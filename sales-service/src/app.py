from flask import Flask, jsonify
from flask_smorest import Api
from flask_cors import CORS

import os
from dotenv import load_dotenv
import logging


from apis.health_bp import health_bp
from api_messages.base_api_error import ApiError


def create_app():
  app = Flask(__name__)

  # Configuración de endpoints OpenAPI y Swagger (flask-smorest).
  app.config['API_TITLE'] = 'API Sales Service'
  app.config['API_VERSION'] = '1.0.0'
  app.config['OPENAPI_VERSION'] = "3.0.2"
  app.config['OPENAPI_JSON_PATH'] = "api-spec.json"
  app.config['OPENAPI_URL_PREFIX'] = "/"
  app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
  app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

  # Inicialización de flask-smorest extension y registro de APIs:
  api = Api(app)
  api.register_blueprint(health_bp)

  # Inicialización de flask-cors extension.
  cors = CORS()
  cors.init_app(app)

  return app


app = create_app()


@app.errorhandler(ApiError)
def handle_exception(err):
  app.logger.error(f"{type(err)} - {err}")
  if err.__cause__ is not None:
    app.logger.error(err.__cause__)

  err_json = jsonify(err.__dict__)

  return err_json, err.code
