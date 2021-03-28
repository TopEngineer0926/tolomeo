import json
import logging
import sys
import unittest
import app.app as App
import requests
import os
import shutil

from pathlib import Path
from unittest import result


def test_health():
    json_response = requests.get("http://0.0.0.0:5000/api/v1/health")
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
    assert 401 == json_response.status_code


def test_get_evidences_gives_not_authenticated_without_token():
    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/evidences", params={"limit": 1, "page": 1}
    )
    assert 401 == json_response.status_code


def test_get_evidences_gives_not_authenticated_with_expired_token():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTY4NDA5NTgsImlhdCI6MTYxNjgzOTE1OCwic3ViIjoxfQ.blxFD9XbaC853qTIAMtQgoEM9aFY4o-eWNXDovMpwwY"
    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/evidences",
        params={"limit": 1, "page": 1},
        headers={"Authorization": "Bearer " + token},
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


def test_get_export_gives_error_when_does_not_exists():
    if os.path.exists(os.environ.get("EXPORT_PATH")):
        os.remove(os.environ.get("EXPORT_PATH"))

    login_response = requests.post(
        "http://0.0.0.0:5000/api/v1/login",
        json={"email": "test@email.com", "password": "testpassword"},
    )
    token = json.loads(login_response.content)["token"]

    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/evidences/export",
        headers={"Authorization": "Bearer " + token},
    )

    assert 404 == json_response.status_code


def test_get_export_gives_export():

    shutil.copyfile(
        Path(__file__).parent / "resources/export.csv", os.environ.get("EXPORT_PATH")
    )

    login_response = requests.post(
        "http://0.0.0.0:5000/api/v1/login",
        json={"email": "test@email.com", "password": "testpassword"},
    )
    token = json.loads(login_response.content)["token"]

    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/evidences/export",
        headers={"Authorization": "Bearer " + token},
    )

    os.remove(os.environ.get("EXPORT_PATH"))
    assert 200 == json_response.status_code


def test_check_status_gives_not_found_error():
    if os.path.exists(os.environ.get("TASK_PATH")):
        os.remove(os.environ.get("TASK_PATH"))

    login_response = requests.post(
        "http://0.0.0.0:5000/api/v1/login",
        json={"email": "test@email.com", "password": "testpassword"},
    )
    token = json.loads(login_response.content)["token"]

    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/tasks/check-status",
        headers={"Authorization": "Bearer " + token},
    )
    assert 404 == json_response.status_code


def test_check_status_gives_response():
    add_task_file()

    login_response = requests.post(
        "http://0.0.0.0:5000/api/v1/login",
        json={"email": "test@email.com", "password": "testpassword"},
    )
    token = json.loads(login_response.content)["token"]

    json_response = requests.get(
        "http://0.0.0.0:5000/api/v1/tasks/check-status",
        headers={"Authorization": "Bearer " + token},
    )
    remove_task_file()
    assert 200 == json_response.status_code


def test_crawl_gives_error_response_conflict():
    add_task_file()

    login_response = requests.post(
        "http://0.0.0.0:5000/api/v1/login",
        json={"email": "test@email.com", "password": "testpassword"},
    )
    token = json.loads(login_response.content)["token"]

    json_response = requests.post(
        "http://0.0.0.0:5000/api/v1/crawl",
        headers={"Authorization": "Bearer " + token},
    )
    remove_task_file()
    assert 409 == json_response.status_code


def add_task_file():
    if os.path.exists(os.environ.get("TASK_PATH")):
        os.remove(os.environ.get("TASK_PATH"))

    with open(os.environ.get("TASK_PATH"), "w") as f:
        f.write("task.id")


def remove_task_file():
    if os.path.exists(os.environ.get("TASK_PATH")):
        os.remove(os.environ.get("TASK_PATH"))
