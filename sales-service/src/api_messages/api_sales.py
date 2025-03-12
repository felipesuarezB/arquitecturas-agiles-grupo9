from api_messages.base_api_error import ApiError


class CustomersList:
  code = 200

  def __init__(self, customers):
    self.customers = customers


class OrderCreated():
  code = 200

  def __init__(self, order_id: str):
    self.message = "Orden creada exitosamente."
    self.order_id = order_id
