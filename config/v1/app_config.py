
"""
    CONTAINS SYSTEM WIDE CONFIGURATIONS AND KEYS
"""

# ---------------------------------------------------
# DATABASE
# ---------------------------------------------------

MYSQL = {
    'host': "localhost",
    'user': "root",
    'password': "00Apassword7",
    'database': "fathat101users"
}

REDIS = {
    "host": "localhost",
    'port': "6379",
    'db': "0",
    'password': "redisrocker"}

# Parameters to connect to the SMTP server for sending emails.
# TODO: Use a different account than "tayfun@" only for automated emails.
SMTP = {
    "host": "some-host",
    "port": 465,
    "sender_email": "some-email-address",
    "sender_password": "some-password"
}


# AUTHENTICATION -

# ---------------------------------------------------
# JWT Json Web Tokens
# ---------------------------------------------------

JWT_ISSUER = "fathat.org"
JWT_ALGORITHM = "HS256"

# NOTE: THESE WILL BE TEMPORARY SECRETS FOR TESTING. NEVER USE THE SAME FOR PRODUCTION

# Default secret used to create all new access JWTs
JWT_SECRET = "0f8014e60a33413b8f1ef6c414a5ed86"

JWT_REFRESH_SECRET = "0f8014e60a33413b8f1ef6c414a7ab21"

# Default secret used to create all new email JWTs
JWT_EMAIL_SECRET = "0h1014e60a33313b8f1ef6c414a5ed19"

# Default secret for password utilities
JWT_PASSWORD_SECRET = "0f8014e60a33413b8f1ef6c414a1de15"

# ---------------------------------------------------

# Default claims payloads for standard tokens
JWT_BASIC_PAYLOAD_CLAIM = ['user_id', 'standard_claim']

# Default claims payload for email JWTs
JWT_EMAIL_PAYLOAD_CLAIM = ['user_id', 'email_claim']

# Default claims payload for email JWTs
JWT_PASSWORD_PAYLOAD_CLAIM = ['user_id', 'password_claim']

# Default claims payload for refresh JWTs
JWT_REFRESH_PAYLOAD_CLAIM = ['user_id', 'refresh_claim']


# --------------------------------------------------

# Number of hours a standard API usage token lasts
JWT_ACCESS_HOURS = 10
# Number of hours an API refresh token lasts
JWT_REFRESH_HOURS = 24
# Number of hours an API password token lasts
JWT_PASSWORD_HOURS = 1
# Number of hours an API email token lasts
JWT_EMAIL_HOURS = 1

# ---------------------------------------------------
# GENERAL SECTION
# ---------------------------------------------------

# CHANGE TO FALSE TO PREVENT VISITS BEING LOGGED
LOG_VISIT = True

# SYSTEM
DEBUG = False
