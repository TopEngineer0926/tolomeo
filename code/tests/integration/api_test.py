import json
import logging
import sys
import unittest
from unittest import result

import app.app as App
import requests

def test_health():
    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/health"
    )
    assert 200 == json_response.status_code
    assert "OK" == json.loads(json_response.content)


def test_login_gives_token():
    json_response = requests.post(
        "http://0.0.0.0:5000/api/v1/login",
        json={"email": "test@email.com", "password": "testpassword"},
    )
    assert "success" == json.loads(json_response.content)["status"]


def test_login_gives_error_on_wrong_credentials():
    json_response = requests.post(
        "http://0.0.0.0:5000/api/v1/login",
        json={"email": "test@email.commmm", "password": "testpassword"},
    )
    assert 403 == json_response.status_code


def test_get_evidences_gives_not_authenticated_without_token():
    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/evidences", params={"limit": 1, "page": 1}
    )
    assert 401 == json_response.status_code


def test_get_evidences_gives_response_with_token():
    login_response = requests.post(
        "http://0.0.0.0:5000/api/v1/login",
        json={"email": "test@email.com", "password": "testpassword"},
    )
    token = json.loads(login_response.content)["token"]

    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/evidences",
        headers={"Authorization": "Bearer " + token},
        params={"limit": 1, "page": 1},
    )
    assert 200 == json_response.status_code
