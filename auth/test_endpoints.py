from unittest import TestCase
from core import generate_jwt
from endpoints import decode_token, decode_refresh_token


class Test(TestCase):

    def test_decode_token(self):
        token = generate_jwt(user_id=1, access_role='basic', payload_claim={'standard_claim': True})
        payload = decode_token(token)
        self.assertIs(isinstance(payload, dict), True)

    def test_decode_refresh_token(self):
        token = generate_jwt(user_id=1, access_role='basic', payload_claim={'refresh_claim': True})
        payload = decode_refresh_token(token)
        self.assertIs(isinstance(payload, dict), True)
