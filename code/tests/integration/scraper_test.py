import unittest
from unittest import result
import requests
from http import client
import logging
import sys
import json
import os
import uuid
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

def test_detective_return_none_if_steps_are_over(caplog):
    caplog.set_level(logging.INFO)
    urls = ['https://www.facebookcorewwwi.onion/'] #http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page # hidden wiki
    detective = Detective()
    evidence = detective.investigate(urls_list=urls, keywords=['drug', 'porn'], step=2, total_steps=1)
    assert None == evidence

def test_detective_return_none_if_url_already_scraped_and_was_only_one(caplog):
    caplog.set_level(logging.INFO)
    repo_client=Repository(adapter=PostgresRepository)
    puppet_uuid = str(uuid.uuid4())
    puppet_evidence = {
        'uuid': puppet_uuid,
        'parent': None,
        'keywords': ','.join(['drug', 'porn']),
        'source': "website",
        'step': 1,
        'total_steps': 1,
        "url": "https://www.facebookcorewwwi.onion/",
        "title": "",
        "urls_found": [],
        "urls_queryable": [],
        "keywords_found": [],
    }
    repo_client.save_evidence(puppet_evidence)
    urls = ['https://www.facebookcorewwwi.onion/'] #http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page # hidden wiki
    detective = Detective()
    evidence = detective.investigate(urls_list=urls, keywords=['drug', 'porn'])
    repo_client.delete_evidence(puppet_uuid)
    assert None == evidence
    
# # TODO: edit test to check by url on db
# def test_detective_investigate_snowball(caplog):
#     caplog.set_level(logging.INFO)
#     urls = ['http://dirnxxdraygbifgc.onion'] #http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page # hidden wiki
#     detective = Detective()
#     detective.investigate(urls_list=urls, keywords=['cocaina','eroina','purezza'], total_steps=2)
#     repo_client=Repository(adapter=PostgresRepository)
#     db_evidence = repo_client.find_evidence(evidence['uuid'])
#     assert evidence['uuid'] == db_evidence[0]
#     assert urls[0] == db_evidence[8]

def test_service_creates_new_user():
    user_repo = UserSchema().load({'email': 'pippo@email.com'})
    response = Service().create_user(user_repo)
    assert 'pippo@email.com' == response['email']

    users = Service().find_all_users('pippo@email.com')
    assert len(users) > 0

    deleted = Service().delete_user_for('pippo@email.com')
    assert True == deleted

def test_creates_postgres_user():
    service = Service(repo_client=Repository(adapter=PostgresRepository))
    user_repo = UserSchema().load({'email': 'pippo@email.com'})
    response = service.create_user(user_repo)
    assert 'pippo@email.com' == response['email']

    users = service.find_all_users('pippo@email.com')
    assert len(users) > 0

    deleted = service.delete_user_for('pippo@email.com')
    assert True == deleted
