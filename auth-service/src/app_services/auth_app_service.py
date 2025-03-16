from flask import current_app as app
from flask_jwt_extended import create_access_token

from repositories import users_repository
from models.authentication import UserCredentialsJson, UserToken, UserProfile
from api_messages.api_auth import InvalidUserCredentials, UserAuthenticated, TokenValidated

import os
from datetime import timedelta


class AuthAppService:

  def __init__(self):
    pass

  def authenticate_user(self, user_creds: UserCredentialsJson):
    if not users_repository.exists_user_with_credentials(user_creds):
      raise InvalidUserCredentials()

    token = create_access_token(user_creds['username'],
                                expires_delta=timedelta(days=7),
                                additional_claims={'user_role': 1})

    return UserAuthenticated(token)

  def validate_token(self, user_token: UserToken):
    user_profile = users_repository.lookup_user_profile_by_username(user_token.username)

    return TokenValidated(str(user_profile.user_id))
