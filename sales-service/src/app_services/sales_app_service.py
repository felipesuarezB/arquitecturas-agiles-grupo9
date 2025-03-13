import uuid

from repositories import customers_repository, orders_repository
from models.customers import Customer, CustomerJson
from models.orders import Order, OrderEventLog, NewOrderCommandJson
from api_messages.api_sales import CustomersList, OrderCreated


class SalesAppService:

  def __init__(self):
    pass

  def list_customers(self):
    customers = customers_repository.find_customers()
    customers_json = [CustomerJson().dump(customer) for customer in customers]

    return CustomersList(customers_json)

  def create_order(self, new_order_cmd: NewOrderCommandJson):
    order = Order()
    orders_repository.create_order(order)
    #evet_log = createLog(order)
    
    return OrderCreated(order.id)
