from scheduler import scheduler

from app_services import client_app_service


@scheduler.task(trigger='interval', id='client_job', seconds=10,
                max_instances=1, coalesce=True, misfire_grace_time=900)
def client_job():
  with scheduler.app.app_context():
    client_app_service.simulate_client_requests()
