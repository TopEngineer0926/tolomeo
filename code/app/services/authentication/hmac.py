import os
import hashlib
import hmac


class HmacAuth(object):
    def __init__(self, *args):
        self.secret_key = os.environ.get("HMAC_SECRET")

    def hexdigest_message(self, message):
        internal_hmac = hmac.new(
            message.encode(), self.secret_key.encode(), hashlib.sha256
        )
        return internal_hmac.hexdigest()

    def is_valid_hexdigest(self, hexdigest, message):
        expected_hexdigest = self.hexdigest_message(message)
        return hmac.compare_digest(expected_hexdigest, hexdigest)
