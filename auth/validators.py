
# -*- coding: utf-8 -*-

"""
    Any Security validators are found here
"""

# ------------------------------
#  Python Imports
# ------------------------------


# ------------------------------
#  External Imports
# ------------------------------
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash as Argon2InvalidHash, VerificationError as Argon2VerificationError

# ------------------------------
#  Local Imports
# ------------------------------


# ------------------------------
#  Validator Functions
# ------------------------------

# ------------------------------------------------
#     Auth Utility Functions
# ------------------------------------------------

def prep_password(password: str):
    """
        Hashes a password
        Password is validated via openapi spec

    :param password:
    :return: Hashed password
    """
    return PasswordHasher().hash(password)


def check_password(password: str, password_hash: str) -> bool:
    """
        Check a password

    :param password:
    :param password_hash:
    :return:
    """
    try:
        return PasswordHasher().verify(password_hash, password)
    except (Argon2VerificationError, Argon2InvalidHash):
        return False


