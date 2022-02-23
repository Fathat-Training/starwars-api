from unittest import TestCase
from starwars import StarWars
from utils import read_json_file


class TestStarWars(TestCase):
    """
        Tests the two main Starwars api request types, the async one with and without batch and max sizes
    """
    def test_request_data_sync(self):
        starwars = StarWars()
        starwars.request_data_sync('films/1')
        assert starwars.swars_data['title'] == "A New Hope"

    def test_request_data_async(self):
        starwars = StarWars()
        starwars.request_data_async('films')
        control_set = read_json_file('starwars-backup-data/films.json')
        assert starwars.swars_data == control_set['results']

    def test_request_data_async_batch_max(self):
        starwars = StarWars()
        starwars.request_data_async('people', 10, 10)
        assert len(starwars.swars_data) == 10
