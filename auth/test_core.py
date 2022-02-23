from unittest import TestCase
from auth.core import generate_jwt, decode_auth_token, verify_payload, permission
from config.v1.app_config import JWT_SECRET, JWT_REFRESH_SECRET, JWT_EMAIL_SECRET


class Test(TestCase):

    def test_generate_jwt_standard(self):
        token = generate_jwt(user_id=1, access_role='basic', payload_claim={'standard_claim': True})
        payload = decode_auth_token(token, JWT_SECRET)
        assert payload['user_id'] == 1 and payload['access_role'] == 'basic'
        assert verify_payload(payload, 'basic')

    def test_generate_jwt_refresh(self):
        token = generate_jwt(user_id=1, access_role='basic', payload_claim={'refresh_claim': True})
        payload = decode_auth_token(token, JWT_REFRESH_SECRET)
        assert payload['user_id'] == 1 and payload['access_role'] == 'basic'
        assert verify_payload(payload, 'basic')

    def test_generate_jwt_email(self):
        token = generate_jwt(user_id=1, access_role='basic', payload_claim={'email_claim': True})
        payload = decode_auth_token(token, JWT_EMAIL_SECRET)
        assert payload['user_id'] == 1 and payload['access_role'] == 'basic'
        assert verify_payload(payload, 'basic')

    def test_pemissions(self):
        token = generate_jwt(user_id=1, access_role='basic', payload_claim={'standard_claim': True})
        payload = decode_auth_token(token, JWT_SECRET)
        assert payload['user_id'] == 1 and payload['access_role'] == 'basic'
        assert permission(payload, 'basic')
