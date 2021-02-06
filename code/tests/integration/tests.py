import unittest
from unittest import result
import requests
from http import client
import logging
import sys
import json
import os
from app.scraper.service import Service
from app.scraper.schema import UserSchema

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

    ## make sure it's working
def test_true():
    a = True
    assert True == a, "Must Be true"

def test_service_creates_new_user():
    user_repo = UserSchema().load({'email': 'pippo@email.com'})
    response = Service().create_user(user_repo)
    assert 'pippo@email.com' == response['email']

    users = Service().find_all_users('pippo@email.com')
    assert len(users) > 0

    deleted = Service().delete_user_for('pippo@email.com')
    assert True == deleted
