# -*- coding: utf-8 -*-

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#    External Imports
# ------------------------------------------------

# ------------------------------------------------
#     Module Imports
# ------------------------------------------------
from starwars import StarWars
from utils import options_filter


# ------------------------------------------------
#     Abstract Character Data Access Layer
# ------------------------------------------------

class FilmDacc(object):
    """
        Abstract Film Data Access Class
    """

    @staticmethod
    def film(film_id, options):
        """
             Retrieve a specific StarWars Film
        :param film_id:
        :param options: The options for filtering what gets returned - See API Specification
        :return: The filtered film data
        """
        starwars = StarWars()
        # Build and request the URL by adding the film_id
        starwars.request_data_sync('films/'+film_id)
        return options_filter(starwars.swars_data, options)[0]

    @staticmethod
    def films(options, max_items, batch_size ):
        """
             Retrieve StarWars Films

        :param batch_size: The size of the batch to get with each async call
        :param max_items: The total amount of items to retrieve over all calls
        :param options:The options for filtering what gets returned - See API Specification
        :return: The filtered films data
        """
        starwars = StarWars()
        starwars.request_data_async('films', batch_size, max_items)
        films = options_filter(starwars.swars_data, options)
        return films, len(films)
