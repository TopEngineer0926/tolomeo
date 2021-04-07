import json
import logging
import os
import sys
import unittest
import uuid
from http import client
from unittest import result

import requests
from app.repository import Repository
from app.repository.postgres import PostgresRepository
from app.scraper.detective import Detective
from app.scraper.service import Service

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
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
    urls = ["https://www.facebookcorewwwi.onion/"]
    detective = Detective()
    evidence = detective.investigate(
        urls_list=urls, keywords=["drug", "porn"], step=2, total_steps=1
    )
    assert None == evidence


def test_detective_return_none_if_url_already_scraped_and_was_only_one(caplog):
    caplog.set_level(logging.INFO)
    repo_client = Repository(adapter=PostgresRepository)
    puppet_uuid = str(uuid.uuid4())
    puppet_evidence = {
        "uuid": puppet_uuid,
        "parent": None,
        "keywords": ",".join(["drug", "porn"]),
        "source": "website",
        "step": 1,
        "total_steps": 1,
        "url": "https://www.facebookcorewwwi.onion/",
        "title": "",
        "urls_found": [],
        "urls_queryable": [],
        "keywords_found": [],
        "has_form": False,
        "has_input_password": False,
    }
    repo_client.save_evidence(puppet_evidence)
    urls = ["https://www.facebookcorewwwi.onion/"]
    detective = Detective()
    evidence = detective.investigate(urls_list=urls, keywords=["drug", "porn"])
    repo_client.delete_evidence(puppet_uuid)
    assert True == evidence
