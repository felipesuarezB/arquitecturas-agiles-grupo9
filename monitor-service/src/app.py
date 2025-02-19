from flask import Flask, jsonify
from flask_smorest import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import os
from dotenv import load_dotenv
import logging

from database import db, get_postgresql_url
from scheduler import scheduler

from apis.health_bp import health_bp
from apis.experimentos_bp import experimentos_bp
from jobs.monitor_job import monitor_job
from api_messages.base_api_error import ApiError
from api_messages.api_errors import TokenNotFound, TokenInvalidOrExpired


def create_app():
  app = Flask(__name__)

  # Configuración de endpoints OpenAPI y Swagger (flask-smorest).
  app.config['API_TITLE'] = 'API Monitor Service'
  app.config['API_VERSION'] = '1.0.0'
  app.config['OPENAPI_VERSION'] = "3.0.2"
  app.config['OPENAPI_JSON_PATH'] = "api-spec.json"
  app.config['OPENAPI_URL_PREFIX'] = "/"
  app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
  app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

  # Inicialización de flask-smorest extension y registro de APIs:
  api = Api(app)
  api.register_blueprint(health_bp)
  api.register_blueprint(experimentos_bp)

  # Configuración de base de datos con SQLAlchemy (flask-sqlalchemy).
  if os.getenv('ENVIRONMENT') in ['test']:
    database_uri = ''
    if os.getenv('DB_HOST') in ['memory']:
      database_uri = 'sqlite:///:memory:'
    elif os.getenv('DB_HOST') in ['sqlite']:
      database_uri = 'sqlite:///test.db'
    else:
      database_uri = get_postgresql_url()
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.logger.setLevel(logging.DEBUG)
  else:
    app.config['SQLALCHEMY_DATABASE_URI'] = get_postgresql_url()

    app.logger.setLevel(logging.INFO)

  # Inicialización flask-sqlalchemy extension y creación de esquemas de base de datos.
  db.init_app(app)
  with app.app_context():
    db.create_all()

  # Inicialización de flask-cors extension.
  cors = CORS()
  cors.init_app(app)

  # Configuración de variables para manejo de tokens JWT (flask-jwt-extended).
  app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

  # Inicialización de flask-jwt-extended extension.
  jwt = JWTManager()
  jwt.init_app(app)

  # Configuración de flask-apscheduler.
  app.config['SCHEDULER_API_ENABLED'] = False

  # Inicialización de flask-apscheduler.
  scheduler.init_app(app)
  scheduler.start()

  return app, jwt


app, jwt = create_app()


@app.errorhandler(ApiError)
def handle_exception(err):
  app.logger.error(f"{type(err)} - {err}")
  if err.__cause__ is not None:
    app.logger.error(err.__cause__)

  err_json = jsonify(err.__dict__)

  return err_json, err.code


@jwt.unauthorized_loader
def unauthorized_callback(reason):
  app.logger.error(f"unauthorized_loader: {reason}")

  err = TokenNotFound()
  err_json = jsonify(err.__dict__)

  return err_json, err.code


@jwt.invalid_token_loader
def invalid_token_callback(reason):
  app.logger.error(f"invalid_token_loader: {reason}")

  err = TokenInvalidOrExpired()
  err_json = jsonify(err.__dict__)

  return err_json, err.code


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
  err = TokenInvalidOrExpired()
  err_json = jsonify(err.__dict__)

  return err_json, err.code
