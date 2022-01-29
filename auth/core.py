# -*- coding: utf-8 -*-

# ----------------------------
#  Python Imports
# ----------------------------
import datetime
import uuid
import sys
import os

# ----------------------------
#  Third Party Imports
# ----------------------------
import jwt

# ----------------------------
#  Module Imports
# ----------------------------
from auth.schemas import access_roles

# ----------------------------
#  Module Imports
# ----------------------------
from errors.v1.handlers import ApiError
from config.v1.app_config import JWT_SECRET, JWT_EMAIL_SECRET, JWT_REFRESH_SECRET, JWT_PASSWORD_SECRET, JWT_BASIC_PAYLOAD_CLAIM, \
    JWT_EMAIL_PAYLOAD_CLAIM, JWT_PASSWORD_PAYLOAD_CLAIM, JWT_REFRESH_PAYLOAD_CLAIM, JWT_ISSUER, JWT_ALGORITHM, \
    JWT_ACCESS_HOURS, JWT_REFRESH_HOURS, JWT_EMAIL_HOURS, JWT_PASSWORD_HOURS
from database.redis.rd_utils import redis_connection

# ----------------------------
#  path settings
# ----------------------------
module_path = os.path.abspath(os.getcwd())

if module_path not in sys.path:
    sys.path.append(module_path)


DEFAULT_PAYLOAD = ['iat', 'sub', 'exp']


# ----------------------------
#  Functions
# ----------------------------

def generate_jwt(**kwargs: dict) -> str:
    """
        Generate a JWT for api call usage

    :param kwargs: must contain access_role and user_id
    :return: token
    :errors:
        'invalid-payload_CLAIM_argument' 401
        'problem-encoding-jwt' 401
        'missing-users-id-for-token-generation' 401
    """

    def gen_token(**kwargs: dict) -> str:
        """
            Generates a payload
            
        :param kwargs:
        :return: usage payload
        """
        payload = {}

        try:

            # payload_claim states the kind of claim i.e. standard_claim, refresh_claim, email_claim, password_claim etc
            if kwargs.get('payload_claim') and isinstance(kwargs['payload_claim'], dict):

                claims = kwargs['payload_claim']

                if kwargs.get('hours'):
                    hours = kwargs.get('hours')
                elif claims.get('standard_claim'):
                    hours = JWT_ACCESS_HOURS
                elif claims.get('refresh_claim'):
                    hours = JWT_REFRESH_HOURS
                elif claims.get('email_claim'):
                    hours = JWT_EMAIL_HOURS
                elif claims.get('password_claim'):
                    hours = JWT_PASSWORD_HOURS
                else:
                    raise Exception

                payload.update(kwargs['payload_claim'])

            else:
                raise ApiError('invalid-token', status_code=401)

            payload.update({
                'iss': JWT_ISSUER,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=hours),
                'iat': datetime.datetime.utcnow(),
                'sub': str(uuid.uuid4()),
                'access_role': kwargs['access_role'],
                'user_id': kwargs['user_id']
            })

            # get the secret
            if select_secret(payload):
                # Encode the token
                token = jwt.encode(
                    payload,
                    select_secret(payload),
                    algorithm=JWT_ALGORITHM)

                return token
            else:
                raise ApiError('invalid-token', status_code=401)

        except Exception as e:
            raise ApiError('token-generation-failure', status_code=401)

    if kwargs['user_id']:

        token = gen_token(**kwargs)
        return token
    else:
        raise ApiError('user-not-found', status_code=401)


def decode_auth_token(token: str, secret: str) -> dict:
    """
    Decodes the auth token
    :param secret:
    :param token:
    :return: returns the payload of the decoded JWT
    :errors:
        'token-expired' 401
        'token-invalid' 401
    """
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ApiError('token-expired', status_code=401)
    except jwt.InvalidTokenError:
        raise ApiError('token-invalid', status_code=401)


def has_expired(token: str, secret: str):
    """
        Helper function to test if a token has expired without raising an ApiError

    :param token:
    :param secret:
    :return:
    """
    try:
        jwt.decode(token, secret, algorithms=['HS256'])
        return False
    except jwt.ExpiredSignatureError:
        return True


def decode_usage_token(token: str):
    """
        Decodes an email token
    :param token:
    :return: returns the payload of the decoded JWT
    :errors: See decode_auth_token
    """
    return decode_auth_token(token, JWT_SECRET)


def decode_email_token(token: str):
    """
        Decodes an email token

    :param token:
    :return: returns the payload of the decoded JWT
    :errors: See decode_auth_token

    """
    return decode_auth_token(token, JWT_EMAIL_SECRET)


def decode_password_token(token: str):
    """
        Decodes a password token

    :param token:
    :return: returns the payload of the decoded JWT
    :errors: See decode_auth_token

    """
    return decode_auth_token(token, JWT_PASSWORD_SECRET)


def revoke_auth_token(token: str):
    """
        This could be used when a user logs out.
        Save a token to redis cache.
        TODO: We need a cron job to clear out expired tokens

    :param cid: Client ID
    :param token:
    :return:
    """
    redis_connection.set(token)


def is_revoked(token: str) -> bool:
    """

        Checks Redis cache for a revoked token. The issue here is when Redis cache fails...without a model we can't back this up.
        If we have a model then we will hit it for every single current non-revoked token, so a lot.
        If we have short-lived tokens we would not require this. However, we cannot expect users to login every 5 minutes so we would need to use a refresh token
        to allow generation of a new access token. The refresh token would then need to be refreshed itself after users.

        We would require a cron job to clear this out on a regular basis.

    :param cid: Client ID
    :param token: Client token
    :return: True if revoked or False
    """
    if redis_connection.get(token):
        return True

    return False


def verify_payload(payload: dict, access_role: str) -> bool:
    """
        Verify the payload against the payload claims - making sure all is present and correct

    :param payload:
    :param access_role:
    :return: True
    :errors:
        'authorisation-required' 401
        'token-invalid' 401
    """
    if payload:
        # Check if all claims are present in payload keys
        # Raise an error

        if 'standard_claim' in payload:
            claims = JWT_BASIC_PAYLOAD_CLAIM
        elif 'email_claim' in payload:
            claims = JWT_EMAIL_PAYLOAD_CLAIM
        elif 'password_claim' in payload:
            claims = JWT_PASSWORD_PAYLOAD_CLAIM
        elif 'refresh_claim' in payload:
            claims = JWT_REFRESH_PAYLOAD_CLAIM
        else:
            raise ApiError('token-invalid', status_code=401)

        if len(set(claims) - set(payload.keys())):
            raise ApiError('token-invalid', status_code=401)

        # Check that the payload from the token has the minimum_role required
        if access_role:
            roles = access_roles()
            if roles[payload['access_role']] < roles[access_role]:
                raise ApiError('authorisation-required', status_code=401)

        return True
    else:
        raise ApiError('token-invalid', status_code=401)


def verify_email_token(token: str):
    """
        Verifies an email JWT token
    :param token:
    :returns: Token payload dictionary
    """
    if not is_revoked(token):
        payload = decode_email_token(token)
        access_role = payload["access_role"]
        verify_payload(payload, access_role)

        return payload

    return False


def select_secret(payload: dict) -> str | bool:
    """
        Returns a specific secret based on the contents of payload

    :param payload:
    :return:  secret or False
    """
    if payload.get('email_claim'):
        return JWT_EMAIL_SECRET
    elif payload.get('password_claim'):
        return JWT_PASSWORD_SECRET
    elif payload.get('refresh_claim'):
        return JWT_REFRESH_SECRET
    elif payload.get('standard_claim'):
        return JWT_SECRET

    return False


def permission(payload: dict, access_role: str, logout=False) -> bool:
    """
        Called from our endpoints prior to code access.

    :param payload: token_info passed via the endpoint:
    :param access_role: The access role of the client attempting access
    :param logout: If True then client is logging out
    :return: Boolean - True
    """
    verify_payload(payload, access_role)

    if logout:
        revoke_auth_token(payload['token'])

    return True
