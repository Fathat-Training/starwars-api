

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#    External Imports
# ------------------------------------------------

# ------------------------------------------------
#     Project Imports
# ------------------------------------------------
from starwars import StarWars
from utils import options_filter, dict_sort

# ------------------------------------------------
#     local VARIABLES
# ------------------------------------------------


# ------------------------------------------------
#     Abstract Character Data Access Layer
# ------------------------------------------------

class CharacterDacc(object):
    """
        Abstract Character Data Access Class
    """

    @staticmethod
    def character(character_id: str, options) -> dict:
        """
             Retrieve a specific StarWars Character
        :param character_id:
        :param options: The options for filtering what gets returned - See API Specification
        :return:
        """
        starwars = StarWars()
        starwars.request_data_sync('people/'+character_id)
        return options_filter(starwars.swars_data, options)[0]

    @staticmethod
    def characters(kwargs: dict) -> tuple[list, int] | tuple[list[dict], int]:
        """
             Retrieve StarWars Characters

        :param kwargs:
             options - object of option key-value pairs for returning extra data based on a boolean value for each key. See Api Specification for Character options
             sort_by - Optional string to use for sorting results
             sort_order - Optional string to sort results in either ascending or descending order
             max_items - The maximum items to return across all batches
             batch_size - The maximum number of items for each api call to be returned
        :return:
        """
        # From research we know that there are roughly 82 characters in the api database ( might change with the next movie release). We want to return
        # all of the people. Now given that there are currently only 82 it would be a simple process to make one call to the api and receive all of the
        # characters in one hit. However, what if we are dealing with thousands or even millions of character records. Returning them all at once would
        # our Request would take quite a long time, so what we shall do is to ...
        # To speed things up we generate all the api calls upfront as asynchronous calls.

        # NOTE: this is not the same as pagination!
        starwars = StarWars()
        starwars.request_data_async('people', kwargs['batch_size'], kwargs['max_items'])
        data = options_filter(starwars.swars_data, kwargs['options'])

        if kwargs.get('sort_by'):
            sort_order = kwargs['sort_order'] or "asc"
            sorted_data = dict_sort(data, kwargs['sort_by'], sort_order)
            return sorted_data, len(sorted_data)

        return data, len(data)
