# -*- coding: utf-8 -*-

# ------------------------------
#  External Imports
# ------------------------------
from flask import Blueprint
from flask import jsonify

# ------------------------------
#  Python Imports
# ------------------------------
import logging

# ------------------------------
#  Module Imports
# ------------------------------


# ------------------------------
#  Flask Blueprint Declaration
# ------------------------------
error_handlers = Blueprint('error_handlers', __name__)


# ------------------------------
#  Error Classes
# ------------------------------

class ApiError(Exception):
    """
        Parent Error Class - inherits default Exception
    :param: Exception - The raised exception
    """
    def __init__(self, message='There was an error', status_code=500, payload=None):
        """
        Class
        :param message: String
        :param status_code: Integer
        :param payload: Dict
        """
        Exception.__init__(self)
        self.message = message

        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        super(ApiError, self).__init__(message, status_code, payload)

    def to_dict(self):
        """
            Convert payload to a dictionary and add the message
        :return:
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = "error"
        return rv


class DataAccessError(Exception):
    """
       Indicates that there is some form of data access error in our data access layers
    :param: Exception
    """
    def __init__(self, **kwargs):
        self.message = kwargs['message']
        self.status_code = kwargs['status_code']
        self.payload = kwargs.get('payload') or None
        super(DataAccessError, self).__init__(self.message, self.status_code)


@error_handlers.app_errorhandler(ApiError)
def handle_api_error(error):
    """
        Handles and logs the ApiError
    :param error: The actual error
    :return: error response
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    logging.error(str(response.json['message']))
    return response
