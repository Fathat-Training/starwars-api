from unittest import TestCase

from auth.utils import prep_password, check_password


class Test(TestCase):

    def test_password_correct(self):
        pwd = prep_password("00Apassword7")
        result = check_password("00Apassword7", pwd)
        self.assertIs(result, True)

    def test_password_incorrect(self):
        pwd = prep_password("00Apassword7")
        result = check_password("00Apassword", pwd)
        self.assertIs(result, False)
