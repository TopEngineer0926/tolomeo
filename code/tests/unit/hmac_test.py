from app.services.authentication.hmac import HmacAuth


def test_auth_hmac_encode_and_match():
    hmac_test = HmacAuth()
    message = "message"
    hexdigest = hmac_test.hexdigest_message(message)
    assert True == hmac_test.is_valid_hexdigest(hexdigest, message)
