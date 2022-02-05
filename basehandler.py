
# *-* coding: UTF-8 *-*

# ------------------------------------------------
#     Python Library Imports
# ------------------------------------------------

# ------------------------------------------------
#    External Python Library Imports
# ------------------------------------------------

# ------------------------------------------------
#     Module Imports
# ------------------------------------------------

# ------------------------------------------------
#     Module Imports
# ------------------------------------------------


# ------------------------------------------------
#    Base Handling Functions Begin Here
# ------------------------------------------------

def api_response(payload=None) -> dict:
    """
        Generate and return an appropriate response to the API request

    :param payload:
    :return:
    """
    if isinstance(payload, dict):
        return payload
    else:
        return {}



