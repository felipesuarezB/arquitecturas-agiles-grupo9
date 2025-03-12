from models.customers import Customer

import uuid


class CustomersRepository:

  def __init__(self):
    pass

  def find_customers(self):
    customers = [
        Customer(uuid.UUID('32bb1c5e-446e-458c-aded-c9a99a8cd90c'), 'Customer 1'),
        Customer(uuid.UUID('46d4868b-6217-4898-900d-3c4bcaf7744c'), 'Customer 2')
    ]

    return customers
