# -*- coding: utf-8 -*-

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------
from datetime import datetime

# ------------------------------------------------
#    External Imports
# ------------------------------------------------

# ------------------------------------------------
#     Project Imports
# ------------------------------------------------
from errors.v1.handlers import ApiError
from auth.utils import check_password
from auth.core import generate_jwt, decode_access_token, revoke_auth_token
from database.mysql.db_utils import db_insert_update, db_query, db_delete
from database.redis.rd_utils import redis_connection
from utils import send_email

from flask import request
import urllib.parse

# ------------------------------------------------
#     Abstract User Data Access Layer
# ------------------------------------------------


class UserDacc(object):
    """
        Abstract User Data Access Class
    """

    @staticmethod
    def signup(data):
        """
            Create and save a new user

        :param data:
        :return:
        """
        # Check if there is an existing user with the same email
        if UserDacc.user_exists_by_email(data['email']):
            raise ApiError(message="user-already-exists", status_code=400)

        sql = "INSERT INTO users (email, password, access_role, created, disabled, email_verified, logged_in) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (data['email'], data['password'], data['access_role'], datetime.now(), 0, 0, 0)
        db_insert_update(sql, values)

        # Retrieve the newly created user and send verification email.
        user = UserDacc.get_by_email(data['email'])
        UserDacc.send_verification_email(user)

    @staticmethod
    def login(email: str, password: str):
        """

        :param email:
        :param password:
        :return:
        """
        try:
            user = UserDacc.get_by_credentials(email, password)
        except Exception as e:
            raise ApiError(message="not-found", status_code=404)

        if user['logged_in']:
            raise ApiError(message="user-already-logged-in", status_code=400)

        if not user['disabled']:

            if user['email_verified']:

                # Generate new access and refresh tokens
                token, refresh_token = UserDacc.generate_new_tokens(user['id'])

                # Update the record to state user logged in
                sql = "UPDATE users SET logged_in = %s WHERE id = %s"
                db_insert_update(sql, (1, user['id']))
                return user['id'], token, refresh_token
            else:
                raise ApiError(message="email-unverified", status_code=400)

        else:
            raise ApiError(message="User Account Disabled", status_code=400)

    @staticmethod
    def logout(user_id: str):
        """

        :param user_id:
        :return:
        """
        # Save the new refresh token to the user's database row.
        sql = "UPDATE users SET logged_in = %s WHERE id = %s"
        db_insert_update(sql, (0, user_id))

    #
    # @staticmethod
    # def update(user_id, data):
    #     """
    #         Update a user entity
    #
    #     :param user_id:
    #     :param kwargs:
    #     :return:
    #     """
    #     pass
    #
    # @staticmethod
    # def list_users(kwargs):
    #     """
    #          Lists Users from page in batches - paginated
    #     :param kwargs:
    #     :return:
    #     """
    #     users, pagination_data = ModelHelpers.match_query(User,
    #                                                       filters=kwargs.get('filters'),
    #                                                       sort_by=kwargs.get('sort_by'),
    #                                                       sort_order=kwargs.get('sort_order'),
    #                                                       pagination_data=kwargs.get('pagination'))
    #
    #     return ModelHelpers.model_return(users, True, excludes=USER_EXCLUDES), pagination_data
    #

    @staticmethod
    def get_by_credentials(email, password):
        """
            Fetch a user's entity via credentials

        :param email: User's email
        :param password: User's password
        :return: User's Entity

        :errors:
            'user-not-found', 404
        """
        user = UserDacc.get_by_email(email)

        if check_password(password, user['password']):
            return user
        else:
            raise ApiError(message='forbidden', status_code=403)

    @staticmethod
    def get_by_email(email: str) -> dict:
        """
            Fetch a user's entity by email address

        :param email: User's email
        :return: User's Entity

        :errors:
            'user-not-found', 404
        """
        sql = "SELECT * FROM users WHERE email = %s"
        values = (email,)
        user = db_query(sql, values)[0]

        if user:
            return user

        raise ApiError(message='user-not-found', status_code=404)

    @staticmethod
    def user_exists_by_email(email: str) -> bool:
        """
            Returns True if there is an existing user with the given email address

        :param email: User's email
        :return: True iff the user with email exists
        """
        sql = "SELECT id FROM users WHERE email = %s"
        values = (email,)
        return len(db_query(sql, values)) > 0

    @staticmethod
    def user_exists_by_id(user_id) -> bool:
        """
            Returns True if there is an existing user with the given ID
        :param email: User ID to check if exists
        :return: True iff the user with given ID exists
        """
        sql = "SELECT id FROM users WHERE id = %s"
        values = (user_id,)
        return len(db_query(sql, values)) > 0

    @staticmethod
    def get_by_id(id) -> dict:
        """
            Fetch a user's entity by ID

        :param id: User's ID
        :return: User's Entity

        :errors:
            'user-not-found', 404
        """
        sql = "SELECT * FROM users WHERE id = %s"
        values = (str(id),)
        user = db_query(sql, values)[0]

        if user:
            return user

        raise ApiError(message='user-not-found', status_code=404)

    @staticmethod
    def send_verification_email(user: dict):
        """
            Sends verification email to the given user.

        :param user: User to send the email.
        """
        token = UserDacc.get_token(user_id=user['id'], access_role=user['access_role'], payload_claim={'email_claim': user['email']})

        params = {'token': token}
        verification_url = f"{request.url_root}users/v1/email_verification?" + urllib.parse.urlencode(params)

        message_body = f"""Please verify account for {user['email']} by clicking on the following link:
            {verification_url}
            """

        try:
            send_email(user['email'], "Please verify account", message_body)
        except Exception as e:
            raise ApiError(message="verification-email-not-sent", status_code=500)

    @staticmethod
    def verify_email(user_id, user_email: str):
        """
            Verifies the email of the given user by id

        :param user_id ID of the user
        :param user_email:
        :return: True if the user's email has been verified, or False otherwise
        :errors:
            'user-not-found', 404
        """
        user = UserDacc.get_by_id(user_id)

        # Check if the token contains the current email of the user.
        if user["email"] != user_email:
            raise ApiError(message="token-invalid", status_code=401)

        sql = "UPDATE users SET email_verified = 1 WHERE id = %s"

        db_insert_update(sql, (user_id,))


    @staticmethod
    def get_token(**kwargs: dict) -> str:
        """
            Create a token and return

        :param user_id:
        :param kwargs:
        :return:
        """
        return generate_jwt(**kwargs)

    @staticmethod
    def generate_new_tokens(uid: int, old_access_token=False) -> tuple:
        """
            Generate a new standard token and a new refresh token.

        :param uid: User's ID to generate new tokens for passed from client
        :param old_access_token: The old access token to be revoked.
        """
        try:

            if old_access_token:
                try:
                    old_token_payload = decode_access_token(old_access_token)
                    revoke_auth_token(old_access_token)
                except ApiError as e:
                    if e.message == 'token-invalid':
                        raise e
                if old_token_payload['user_id'] != uid:
                    raise ApiError(message='token-invalid', status_code=403)

            user = UserDacc.get_by_id(uid)

            if user['refresh_token']:
                # Add the old refresh token to some kind of cache (In this case Redis) so
                # that we can fail the token in authorisation if it has not yet expired.
                redis_connection.set(user['refresh_token'])

            token = UserDacc.get_token(user_id=uid, access_role=user['access_role'], payload_claim={'standard_claim': True})
            refresh_token = UserDacc.get_token(user_id=uid, access_role=user['access_role'], payload_claim={'refresh_claim': True})

            # Save the new refresh token to the user's database row.
            sql = "UPDATE users SET refresh_token = %s WHERE id = %s"
            db_insert_update(sql, (refresh_token, user['id']))

            return token, refresh_token

        except Exception as e:
            raise e

    @staticmethod
    def delete_user(user_id):
        """
            Delete a user.
        :param user_id: ID of the user
        """
        sql = "DELETE FROM users WHERE id = %s"
        values = (str(user_id),)
        num_deleted = db_delete(sql, values)
        print(f"deleted row count={num_deleted}")
        if num_deleted == 0:
            raise ApiError(message="not-found", status=404)

    # @staticmethod
    # def revoke_refresh_token(user_id):
    #     """
    #         Revoke a user's refresh token
    #         Normally this should not be called as when a user logs out
    #         When they log back in again a new refresh token shall be issued
    #
    #     :param user_id:
    #     :return:
    #     """
    #     user = UserDacc.get_by_id(user_id)
    #
    #     if user:
    #         # Delete the refresh token from the users entity
    #         refresh_token = user.refresh_token
    #         # Add the token to cache
    #         cache_set(refresh_token, 1)
    #         # DUMP the token from the users entity
    #         user.refresh_token = None
    #
    #         ModelHelpers.update(user)
    #         return user.id
    #
    #     return False
    #
    # @staticmethod
    # def reset_password(user_id, old_password, new_password):
    #
    #     """
    #         Reset a user's password - Requires old and new passwords
    #
    #     :param user_id:
    #     :param old_password:
    #     :param new_password:
    #     :return: True
    #     :errors:
    #         'user-not-found', 404
    #     """
    #     pass
    #
    # @staticmethod
    # def update_password(password, data):
    #     """
    #          Updates a user's password
    #
    #     :param payload:
    #     :param email:
    #     :param password:
    #     :return: True
    #     :errors:
    #         'user-not-found', 404
    #     """
    #     pass
    #
    # @staticmethod
    # def log_user_visit_async(user_id, ip, user_agent):
    #     """
    #         Logs a users's visit asynchronously
    #
    #     :param user_id:
    #     :param ip:
    #     :param user_agent:
    #     :param locale_data:
    #     :return: Returns a future
    #     """
    #     pass
