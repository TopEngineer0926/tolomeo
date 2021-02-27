import unittest
from unittest import result
import requests
from http import client
import logging
import sys
import json
import os
from app.scraper.service import Service
from app.scraper.detective import Detective
from app.scraper.schema import UserSchema
from app.repository import Repository
from app.repository.postgres import PostgresRepository

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

def test_detective_investigate_with_default():
    detective = Detective()
    assert None == detective.investigate()

def test_detective_investigate_with_a_list_of_urls_and_keywords(caplog):
    caplog.set_level(logging.INFO)
    detective = Detective()
    assert None == detective.investigate(urls_list=['https://www.facebookcorewwwi.onion/'], keywords=['drug', 'revenge'])

def test_service_creates_new_user():
    user_repo = UserSchema().load({'email': 'pippo@email.com'})
    response = Service().create_user(user_repo)
    assert 'pippo@email.com' == response['email']

    users = Service().find_all_users('pippo@email.com')
    assert len(users) > 0

    deleted = Service().delete_user_for('pippo@email.com')
    assert True == deleted

def test_version_postgres():
    response = Service(repo_client=Repository(adapter=PostgresRepository)).get_version()
    assert  {'data': ('PostgreSQL 10.15 (Debian 10.15-1.pgdg90+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit',)} == response

def test_creates_postgres_user():
    service = Service(repo_client=Repository(adapter=PostgresRepository))
    user_repo = UserSchema().load({'email': 'pippo@email.com'})
    response = service.create_user(user_repo)
    assert 'pippo@email.com' == response['email']

    users = service.find_all_users('pippo@email.com')
    assert len(users) > 0

    deleted = service.delete_user_for('pippo@email.com')
    assert True == deleted
