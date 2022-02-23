from unittest import TestCase
from utils import dict_excludes, dict_sort, read_json_file

test_dict = {'one': 1, "five": 5, "ten": 10, "two": 2, "fire": "fire", "bird":"Parrot"}
excludes = ["ten", "fire", "two"]
excludes_result = {'one': 1, "five": 5, "bird": "Parrot"}


class Test(TestCase):

    def test_dict_excludes(self):
        result = dict_excludes(test_dict, excludes)
        assert excludes_result == result

    def test_dict_sort_ascending(self):
        data = read_json_file('starwars-backup-data/films.json')
        data_sorted = dict_sort(data['results'], "title", "ascending")
        assert data_sorted[0]['title'] == 'A New Hope'

    def test_dict_sort_descending(self):
        data = read_json_file('starwars-backup-data/films.json')
        data_sorted = dict_sort(data['results'], "title", "desc")
        assert data_sorted[0]['title'] == 'The Phantom Menace'

