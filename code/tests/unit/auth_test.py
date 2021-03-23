import logging
import sys
import unittest
from unittest import result

from app.services.authentication.auth import Auth

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def test_auth_jwt_encode_and_decode():
    auth = Auth()
    user_id = 1
    encoded = auth.encode_auth_token(user_id)
    logging.info(encoded)

    decoded = auth.decode_auth_token(encoded)
    logging.info(decoded)
    assert user_id == decoded
