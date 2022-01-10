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
from auth.validators import *
from basehandler import api_response
from errors.v1.handlers import *


# -----------------------------
#     REST FUNCTIONS
# -----------------------------

def signup(**kwargs):
    """
        Signup a user

        Verify the signup
        TODO: Ok = send email
        Not Ok = abort and return

    :param kwargs:
    :return: user entity
    :errors:
        DataAccessError
        "invalid" 400
        "invalid" 400
    """
    data = kwargs['body']

    pwd = prep_password(data['password'])

    try:
        # Check there is an existing user with the same email
        if UserDacc.user_exists_by_email(data['email']):
            raise ApiError(message="user-already-exists", status_code=400)

        # Swap the password in data for the hashed one
        data['password'] = pwd
        UserDacc.create(data)

        # Retrieve the newly created user and send verification email.
        user = UserDacc.get_by_email(data['email'])
        UserDacc.send_verification_email(user)

        return api_response({})

    except DataAccessError as e:
        raise ApiError(e.message, e.status_code, e.payload)


def login(**kwargs):
    """
        Attempts login with users credentials, email and password

    :param kwargs:
           email:
           password:

    :return: Token, Refresh token and user entity
    :errors:

        DataAccessError
            error_msg from password validation 401
            "user-unknown" 400

        "user-forbidden" 400
        "email-unverified", 400
    """
    auth = kwargs['body']
    email = auth['email'].lower()
    password = auth['password']

    try:
        user, token, refresh_token = UserDacc.login(email, password)
        return api_response({'token': token, 'refresh_token': refresh_token, 'user': user})
    except DataAccessError as e:
        raise ApiError(e.message, status_code=e.status_code, payload=e.payload)


def logout(**kwargs):
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
            return api_response()
        else:
            raise ApiError(message="Authorisation required", status_code=400)

    raise ApiError(message="User NOT logged out", status_code=400)


def email_verification(**kwargs):
    """
        Attempts to verify an email via the email token

    :param kwargs:
    :return: SuccessResponse
    :errors:
        'authorisation-required' 401
    """
    if "token" in kwargs:
        payload = verify_email_token(kwargs['token'])
        UserDacc.verify_email(payload['user_id'], payload['email_claim'])
        revoke_auth_token(kwargs['token'])
        return api_response()
    else:
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


def generate_new_tokens(**kwargs):
    """
        Generates new API usage and refresh tokens
        Generally when a client's access token has epired they can request a
        new set of tokens be generated as long as they have the correct unexpired
        refresh token.

    :param kwargs:
    :return: tokens
    :errors:
        'unknown-user' 404
    """
    pass


def suspend(token_info, resident_id, **kwargs):
    """
        Delete a resident
        TODO - when deleting a resident ensure to delete all other relevant data in related model entities

    :param token_info: contains token payload
    :param resident_id:
    :return: SuccessResponse
    :errors:
        'user-not-found' 404
    """
    permission(token_info, access_role='admin')


def delete_account(token_info, user_id, **kwargs):
    """
        Delete a user if and only if it is the current user
        Used by users to delete their own account
        TODO - when deleting a user we must delete all other data in other model entities

    :param token_info: contains token payload
    :param user_id:
    :return: SuccessResponse
    :errors:
        'user-not-found' 404
    """
    permission(token_info, access_role='admin', logout=True)


def get_user(user_id, **kwargs):
    """
        Fetch a user's entity

    :param user_id: user ID to fetch
    :param kwargs: contains token payload with Client request user_id
    :return: User Entity
    :errors:
        DataAccessError
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

    try:
        # Swap the password in data for the hashed one
        users = UserDacc.list_users(kwargs)
        return api_response({'users': users})
    except DataAccessError as e:
        raise ApiError(e.message, e.status_code, e.payload)

