from models.authentication import UserProfile, UserCredentialsJson

import os
import uuid


class UsersRepository:

  def __init__(self):
    self.credentials_username = os.environ.get('CREDENTIALS_USERNAME', '')
    self.credentials_password = os.environ.get('CREDENTIALS_PASSWORD', '')

  def exists_user_with_credentials(self, user_creds: UserCredentialsJson):
    user_match = user_creds['username'] == self.credentials_username
    password_match = user_creds['password'] == self.credentials_password

    return user_match and password_match

  def lookup_user_profile_by_username(self, username: str):
    return UserProfile(uuid.UUID('62c4641b-92e7-4892-a766-fcd68e9eb848'), username)
