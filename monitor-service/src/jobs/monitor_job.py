import os
import time
from datetime import datetime, timedelta
import uuid
import requests

from models.experimento import EstadoExperimento, EstadoCaso
from services.experiment_service import experiment_service
from scheduler import scheduler


@scheduler.task(trigger='interval', id='monitor_job', seconds=10,
                max_instances=1, coalesce=True, misfire_grace_time=900)
def monitor_job():
  print("--------------- Monitor Job Running ---------------")

  service_url = os.environ.get('SERVICE_URL', 'http://localhost:8081/health/ping')
  monitor_interval = os.environ.get('MONITOR_INTERVAL', 2)
  print(f"service_url = {service_url}")
  print(f"monitor_interval = {monitor_interval}")

  with scheduler.app.app_context():
    result = experiment_service.list_experiments(experiment_states=[EstadoExperimento.PROGRAMADO.value])

    for experiment in result.experiments:
      experiment_service.update_experiment(experiment['id'], experiment_state=EstadoExperimento.EN_PROGRESO.value)
      print(f"Experimento {experiment['id']} EN PROGRESO!")

      num_cases = experiment['numero_casos']
      max_retries = experiment['max_reintentos']
      max_timeout = experiment['max_tiempo_espera_seg']

      print(f"Experimento {experiment['id']}(num_cases={num_cases}, max_retries={max_retries}, max_timeout={max_timeout})")

      for num_case in range(num_cases):
        monitor_loop(experiment['id'], max_retries, max_timeout, service_url, monitor_interval)

      experiment_service.update_experiment(experiment['id'], experiment_state=EstadoExperimento.FINALIZADO.value)
      print(f"Experimento {experiment['id']} FINALIZADO!")


def monitor_loop(experiment_id, max_retries, max_timeout, service_url, monitor_interval):
  case = {
      'id': '',
      'id_experimento': experiment_id,
      'intentos': 0,
      'exitosos': 0,
      'timeouts': 0,
      'fallidos': 0,
      'fecha_inicio': datetime.today()
  }
  result = experiment_service.create_case(case)
  case['id'] = str(result.case_id)
  print(f"Caso {case['id']} EN PROGRESO!")

  fail_detected = False
  fail_counter = 0
  start_time = time.time()

  while not fail_detected:
    case['intentos'] += 1
    try:
      print(f"Caso {case['id']} Enviando petición a {service_url}")
      response = requests.get(service_url, timeout=max_timeout)
      print(f"Caso {case['id']} Respuesta a tiempo - Status Code: {response.status_code}, Response: {response.text}")

      if response.status_code == 200:
        fail_counter = 0
        case['exitosos'] += 1
      else:
        fail_counter += 1
        case['fallidos'] += 1

    except requests.RequestException as ex:
      print(f"Caso {case['id']} Timeout en petición - Exception: {ex}")
      fail_counter += 1
      case['timeouts'] += 1

    experiment_service.update_case(case['id'], case)
    print(f"Caso {case['id']} Actualizado fail_counter={fail_counter}")

    if fail_counter >= max_retries:
      fail_detected = True
      print(f"Caso {case['id']} Falla detectada fail_counter={fail_counter}")
    else:
      time.sleep(monitor_interval)

  end_time = time.time()
  duration = end_time - start_time

  case['fecha_fin'] = datetime.today()
  case['duracion_deteccion'] = duration
  case['estado'] = EstadoCaso.FINALIZADO.value

  experiment_service.update_case(case['id'], case)
  print(f"Caso {case['id']} FINALIZADO!")
