# -*- coding: utf-8 -*-

# ------------------------------------------------
#     GAE Imports
# ------------------------------------------------


# ------------------------------------------------
#    External imports
# ------------------------------------------------

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#    Module Imports
# ------------------------------------------------

# ------------------------------------------------
#    User Data Access layer
# ------------------------------------------------
from characters.v1.data_access import *

# ------------------------------------------------
#     Module Imports
# ------------------------------------------------
from basehandler import api_response
from errors.v1.handlers import ApiError, DataAccessError


# ------------------------------------------------
#          CHARACTER REST FUNCTIONS START HERE
# ------------------------------------------------

def get_character(character_id, **kwargs: dict) -> dict:
    """
        Fetch a character's entity based on character's id and return

    :param character_id: The character id
    :param kwargs: options - object of option key-value pairs for returning extra data based on a boolean value for each key. See Api Specification for Character options
    :return: Character Entity
    :errors:
        DataAccessError - raises an APIError
    """

    try:
        character = CharacterDacc.character(character_id, kwargs['options'])
        return api_response(character)
    except DataAccessError as e:
        raise ApiError(e.message, e.status_code, e.payload)


# ------------------------------------------------
#          ENDPOINT FUNCTIONS START HERE
# ------------------------------------------------

def get_characters(**kwargs: dict) -> dict:
    """
        Fetch all the characters via pagination. If there is a cursor then fetch the next batch of users

    :param kwargs:
         options - object of option key-value pairs for returning extra data based on a boolean value for each key. See Api Specification for Character options
         sort_by - Optional string to use for sorting results
         sort_order - Optional string to sort results in either ascending or descending order
         max_items - The maximum items to return across all batches
         batch_size - The maximum number of items for each api call to be returned
    :return: List of Character Entities
    :errors:
    """
    characters, count = CharacterDacc.characters(kwargs)

    if characters:
        return api_response({
            'results': characters,
            'count': count
            }
        )

    else:
        raise ApiError('characters-not-found', status_code=404)

