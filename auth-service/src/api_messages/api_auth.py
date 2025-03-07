from api_messages.base_api_error import ApiError


class InvalidUserCredentials(ApiError):
  code = 401

  def __init__(self):
    self.message = "Credenciales inválidas."


class UserAuthenticated:
  code = 200

  def __init__(self, token: str):
    self.message = "Usuario autenticado."
    self.token = token


class TokenValidated:
  code = 200

  def __init__(self, user_id: str):
    self.message = "Token validado."
    self.user_id = user_id
