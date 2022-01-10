# -*- coding: utf-8 -*-


# ------------------------------------------------
#    External imports
# ------------------------------------------------

import asyncio
import aiohttp
import requests

# ------------------------------------------------
#    Python Imports
# ------------------------------------------------

# ------------------------------------------------
#     local Imports
# ------------------------------------------------
from errors.v1.handlers import DataAccessError

# ------------------------------------------------
#    Script Wide Variables
# ------------------------------------------------
URL = 'https://swapi.dev/api/'

# ------------------------------------------------
#          CLASSES START HERE
# ------------------------------------------------


class StarWars(object):
    """
        Star Wars object
        Facilitates Async Calls to the swapi api for retrieval of star wars data.
        All methods are static helper functions with the exception of request_data.
        The request_data function is used to retrieve star wars data and called via api
        StarWars class object instance.
    """

    def __init__(self, **kwargs):

        # Variables used for each instance of the class.
        self.swars_data = []

    async def fetch_json(self, session: aiohttp.ClientSession(), url: str, **kwargs):
        """
            Async function to make multiple api calls and fetch json data for each call
            Adding the data when received to the self.swars_data list
        """
        print(f"Requesting {url}")
        resp = await session.request('GET', url=url, **kwargs)
        if resp.status == 200:
            data = await resp.json(content_type=None)
            print(f"Received data for {url}")
            # Put the results data on the end of the list
            self.swars_data.extend(data['results'])
        else:
            error = f"url {url}"
            raise DataAccessError(message=error, status_code=resp.status)

    async def api_query(self, urls, **kwargs):
        """r
            Set up an async task for each url in urls and call the urls asynchronously.
            Asyncio sets up a client connection to handle all the calls to the swapi api.
            Calls fetch_json after each task/url call gets a response
        """
        # Single client session for all the api calls. We use an open HTTP connection for simplicity here. The
        # data is open source...
        client = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

        async with client as session:
            # Create fetch tasks from the urls
            tasks = []

            for url in urls:
                tasks.append(self.fetch_json(session=session, url=url, **kwargs))

            # waits for asyncio.gather() to be completed, required because we want to sort when all data has arrived
            await asyncio.gather(*tasks, return_exceptions=True)
            # await session.close() # This has no effect - need to look into this

    def request_data_async(self, query, batch_size=None, max_items=None):
        """
            This method formats n number of urls with the parameter 'query'

            param: query - the api query parameter i.e. films or people
            param: max_items: The maximum number of items to fetch
            params: batch_size: The maximum items returned across all batches/api calls
        """
        # Create the initial url
        urls = [f"{URL}{query}/"]
        urls_append = urls.append

        if max_items and batch_size:
            for i in range(2, round(max_items / batch_size) + 1):
                urls_append(f"{URL}{query}/?format=json&page={i}")

        # Call the api query function
        asyncio.run(self.api_query(urls))

    def request_data_sync(self, query):
        """
            Request and wait for our data to return
            In this method we are using the requests package to make a simple synchronous API call

        :param query: Contains query parameters for the request
        :return:
        """
        status = ""

        try:
            # Format the url from the main swapi url plus the query/queries
            url = f"{URL}{query}/"
            # make the request
            r = requests.get(url=url)
            # Raise the status to make sure it was successful. If it is not the below exception will occur
            status = r.status_code
            r.raise_for_status()

            # We have success - let's return the data
            # extracting data in json format
            self.swars_data = r.json()

        except requests.ConnectionError as e:
            msg = "OOPS!! Connection Error. Make sure you are connected to a live Internet connection."
            raise DataAccessError(message=msg, status_code=status)
        except requests.Timeout as e:
            msg = "OOPS!! Timeout Error"
            raise DataAccessError(message=msg, status_code=status)
        except requests.HTTPError as e:
            if status == 404:
                msg = "Not Found"
            elif status == 400:
                msg = "Bad Request"
            elif status == 500:
                msg = "Server Error on the Star Wars Api"
            else:
                msg = "Opps Something went wrong!!"
            raise DataAccessError(message=msg, status_code=status)
        except KeyboardInterrupt:
            msg = "Someone closed the program"
            raise DataAccessError(message=msg, status_code=status)

