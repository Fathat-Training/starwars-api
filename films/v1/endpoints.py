# -*- coding: utf-8 -*-

# ------------------------------------------------
#    External imports
# ------------------------------------------------

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#    Module Imports
# ------------------------------------------------
from basehandler import api_response
from errors.v1.handlers import ApiError
from auth.core import permission

# ------------------------------------------------
#    Films Data Access layer
# ------------------------------------------------
from films.v1.data_access import *


# ------------------------------------------------
#          FILM REST FUNCTIONS START HERE
# ------------------------------------------------

def get_film(film_id, **kwargs):
    """
        Fetch a film's entity from its name
    :param film_id: The id of the film to be retrieved
    :return: Film Entity
    :errors:
        APIError
    """
    film = FilmDacc.film(film_id, kwargs['options'])
    return api_response(film)


def get_films(**kwargs):
    """
        Fetch all the films via pagination. If there is a cursor then fetch the next batch of films

    :param kwargs: dictionary object containing keyword arguments
    :return: List of Film Entities and total film count
    :errors:
    """

    permission(kwargs['token_info'], access_role='basic')
    films, count = FilmDacc.films(kwargs['options'])

    if films:
        return api_response({
            'results': films,
            'count': count
        })
    else:
        raise ApiError('films-not-found', status_code=404)
