# -*- coding: utf-8 -*-

# ----------------------------
# Python Imports
# ----------------------------

# ----------------------------
# Flask Imports
# ----------------------------

# ----------------------------
# External Imports
# ----------------------------

# ----------------------------
# Project Imports
# ----------------------------
from users.v1.data_access import *
from auth.core import permission, verify_email_token, revoke_auth_token
from auth.utils import *
from basehandler import api_response
from errors.v1.handlers import *


# -----------------------------
#     REST FUNCTIONS
# -----------------------------

def signup(**kwargs: dict):
    """
        Signup a user

        Verify the signup
        Not Ok = abort and return

    :param kwargs:
    :return: user entity
    :errors:
        ApiError
        "invalid" 400
        "invalid" 400
    """
    data = kwargs['body']

    pwd = prep_password(data['password'])

    # Swap the password in data for the hashed one
    data['password'] = pwd
    UserDacc.create(data)

    return api_response()


def login(**kwargs: dict) -> dict:
    """
        Attempts login with users credentials, email and password

    :param kwargs:
           email:
           password:

    :return: Token, Refresh token and user entity
    :errors:

        ApiError
            error_msg from password validation 401
            "user-unknown" 400

        "user-forbidden" 400
        "email-unverified", 400
    """

    auth = kwargs['body']
    email = auth['email'].lower()
    password = auth['password']

    user, token, refresh_token = UserDacc.login(email, password)
    return api_response({'token': token, 'refresh_token': refresh_token, 'user': user})


def logout(**kwargs: dict):
    """
        Logout:
            Log the user out

        NOTE:
        The access token is not available in the token_info passed via connexion, thus we have to extract it from the
        request headers and append it to the token_ifo in the kwargs.

    :param kwargs:
    :return:
    """

    if 'Authorization' in request.headers:

        # Extract auth data from the authentication header
        auth_data = request.headers['Authorization'].encode('ascii', 'ignore').decode('ascii')

        # Check there is a Bearer token
        if 'Bearer ' in auth_data:
            token = auth_data.replace('Bearer ', '')
            kwargs['token_info']['token'] = token

            permission(kwargs['token_info'], access_role='basic', logout=True)
            UserDacc.logout(kwargs['token_info']['user_id'])
            return api_response()
        else:
            raise ApiError(message="Authorisation required", status_code=400)

    raise ApiError(message="User NOT logged out", status_code=400)


def email_verification(**kwargs: dict):
    """
        Attempts to verify an email via the email token

    :param kwargs:
    :return: SuccessResponse
    :errors:
        'authorisation-required' 401
    """
    try:
        payload = verify_email_token(kwargs['token'])
        UserDacc.verify_email(payload['user_id'], payload['email_claim'])
        revoke_auth_token(kwargs['token'])
        return api_response()
    except Exception:
        raise ApiError('authorisation-required', status_code=401)


def resend_email_verification(token_info, user_id, **kwargs):
    """
        Resend the email verification

    :param token_info: contains token payload
    :param user_id
    :param kwargs:
    :return:
    """
    permission(token_info, access_role='basic')


def reset_password(token_info, user_id, **kwargs):
    """
        Reset the user's password.

    :param token_info: contains token payload
    :param user_id: User's ID
    :param kwargs:
    :return: SuccessResponse
    :errors:
         error_msg from password validation 401
        'failed-to-save-new-password' 401
        'unknown-user' 404
    """
    permission(token_info, access_role='basic')


def forgotten_password(**kwargs):
    """
        Sends an email to the user's email with a link to renew password - Link should be on the react frontend...
    :param kwargs:
    :return: password token
    :errors:
        'unknown-user' 404
    """
    pass


def change_password(**kwargs):
    """
        Changes a user's password
    :param kwargs:
    :return: SuccessResponse
    :errors:
        'unknown-user' 404
    """
    pass


def update(user_id, **kwargs):
    """
        Updates a user with appropriate data

    :param user_id
    :param kwargs:
    :return: tokens
    :errors:
        'unknown-user' 404
    """
    permission(kwargs['token_info'], access_role='admin')


def generate_new_tokens(**kwargs: dict) -> dict:
    """
        Generates new API usage and refresh tokens
        Generally when a client's access token has expired they can request a
        new set of tokens be generated as long as they have the correct unexpired
        refresh token.

    :param user_id: The ID of the user to generate new tokens for.
    :param kwargs:
    :return: tokens
    :errors:
        'unknown-user' 404
    """
    permission(kwargs['token_info'], access_role='basic')
    token, refresh_token = UserDacc.generate_new_tokens(kwargs['token_info']['user_id'], kwargs['old_access_token'])
    return api_response({'token': token, 'refresh_token': refresh_token, 'user': kwargs['token_info']['user_id']})


def suspend(token_info, user_id, **kwargs):
    """
        Suspend aka diable a user

    :param token_info: contains token payload
    :param user_id:
    :return: SuccessResponse
    :errors:
        'user-not-found' 404
    """
    permission(token_info, access_role='user')


def delete_account(token_info, user_id, **kwargs):
    """
        Delete a user account.
        Users cannot delete their own account; only admins can delete an account
        TODO - when deleting a user we must delete all other data in other model entities

    :param token_info: contains token payload
    :param user_id:
    :return: SuccessResponse with deleted user's id
    :errors:
        'user-not-found' 404
    """
    permission(token_info, access_role='admin')

    # Do not allow admins to delete their own accounts, let other admins to that.
    if user_id == token_info['user_id']:
        raise ApiError(message="forbidden", status_code=403)

    if not UserDacc.user_exists_by_id(user_id):
        raise ApiError(message="not-found", status_code=404)

    UserDacc.delete_user(user_id)
    return api_response({'id': user_id})


def get_user(user_id, **kwargs):
    """
        Fetch a user's entity

    :param user_id: user ID to fetch
    :param kwargs: contains token payload with Client request user_id
    :return: User Entity
    :errors:
        ApiError
    """
    permission(kwargs['token_info'], access_role='admin')


def list_users(**kwargs):
    """
        Fetch all the users via pagination.
        Apply filters as defined

    :param kwargs:
    :return: User Entity
    :errors:
    """
    permission(kwargs['token_info'], access_role='admin')

    # Swap the password in data for the hashed one
    users = UserDacc.list_users(kwargs)
    return api_response({'users': users})


