import uuid
import datetime

from repositories import customers_repository, orders_repository
from models.customers import Customer, CustomerJson
from models.orders import Order, OrderEventLog, NewOrderCommandJson, OrderEventLogJson
from api_messages.api_sales import CustomersList, OrderCreated, OrderLogsList


class SalesAppService:

  def __init__(self):
    pass

  def list_customers(self):
    customers = customers_repository.find_customers()
    customers_json = [CustomerJson().dump(customer) for customer in customers]

    return CustomersList(customers_json)

  def create_order(self, new_order_cmd: NewOrderCommandJson):
    # Extraer datos del comando
    date = datetime.datetime.fromisoformat(new_order_cmd.order_date)
    product = new_order_cmd.product
    value = new_order_cmd.value
    
    # Crear orden
    order = orders_repository.create_order(date, product, value)
    
    # Crear log de la orden
    order_log = orders_repository.create_order_log(order.id)
    
    return OrderCreated(order.id)

  def get_order_logs(self):
    logs = orders_repository.get_order_logs()
    logs_json = [OrderEventLogJson().dump(log) for log in logs]
    
    return OrderLogsList(logs_json)
