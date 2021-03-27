import datetime
import logging
import sys
import os
import jwt


class Auth(object):
    def __init__(self, *args):
        self.secret_key = os.environ.get("API_SECRET")

    def generate_token_for_user_id(self, user_id):
        return self.encode_auth_token(user_id)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, minutes=30),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, self.secret_key, algorithm="HS256").decode()
        except Exception as e:
            print(str(e))
            return str(e)

    def decode_auth_token(self, auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, self.secret_key)
            return payload["sub"]
        except jwt.ExpiredSignatureError as e:
            raise e
        except jwt.InvalidTokenError as e:
            raise e
