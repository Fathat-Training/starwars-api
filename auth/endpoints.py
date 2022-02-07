# -*- coding: utf-8 -*-

# ------------------------------
#  External Imports
# ------------------------------

# ------------------------------
#  Python Imports
# ------------------------------

# ------------------------------
#  Module Imports
# ------------------------------
from auth.core import *
from config.v1.app_config import JWT_SECRET, JWT_REFRESH_SECRET
from errors.v1.handlers import ApiError


def decode_token(token: str) -> dict:
    """
        Standard Token decode function.
        If we have a token and the token is not in cache - grab the payload
        Called directly via the openapi spec under  x-bearerInfoFunc: auth.endpoints.decode_token

    :param token:
    :return:
    """
    if is_revoked(token):
        raise ApiError('token-invalid', status_code=401)
    else:
        payload = decode_auth_token(token, JWT_SECRET)
        return payload


def decode_refresh_token(token: str) -> dict:
    """
        Refresh Token decode function.
        If we have a token and the token is not in cache - grab the payload
        Called directly via the openapi spec under  x-bearerInfoFunc: auth.endpoints.decode_token

    :param token:
    :return:
    """
    if is_revoked(token):
        raise ApiError('token-invalid', status_code=401)
    else:
        payload = decode_auth_token(token, JWT_REFRESH_SECRET)
        return payload
