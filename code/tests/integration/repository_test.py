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


def test_repo_get_map(caplog):
    caplog.set_level(logging.INFO)
    repo_client = Repository(adapter=PostgresRepository)
    parent = str(uuid.uuid4())
    puppet_evidence = {
        "uuid": parent,
        "parent": None,
        "keywords": ",".join(["drug", "porn"]),
        "source": "website",
        "step": 1,
        "total_steps": 2,
        "url": "https://www.facebookcorewwwi.onion/",
        "title": "",
        "urls_found": [],
        "urls_queryable": [],
        "keywords_found": [],
        "has_form": False,
        "has_input_password": False,
    }
    repo_client.save_evidence(puppet_evidence)

    puppet_evidence = {
        "uuid": str(uuid.uuid4()),
        "parent": parent,
        "keywords": ",".join(["drug", "porn"]),
        "source": "website",
        "step": 2,
        "total_steps": 2,
        "url": "https://www.facebookcorewwwi.onion/",
        "title": "",
        "urls_found": [],
        "urls_queryable": [],
        "keywords_found": [],
        "has_form": False,
        "has_input_password": False,
    }
    repo_client.save_evidence(puppet_evidence)

    puppet_evidence = {
        "uuid": str(uuid.uuid4()),
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
    evidences_map = repo_client.get_evidences_map(None)
    assert 0 < len(evidences_map)


def test_limit_of_get_evidences(caplog):
    caplog.set_level(logging.INFO)
    repo_client = Repository(adapter=PostgresRepository)
    parent = str(uuid.uuid4())
    puppet_evidence = {
        "uuid": parent,
        "parent": None,
        "keywords": ",".join(["drug", "porn"]),
        "source": "website",
        "step": 1,
        "total_steps": 2,
        "url": "https://www.facebookcorewwwi.onion/",
        "title": "",
        "urls_found": [],
        "urls_queryable": [],
        "keywords_found": [],
        "has_form": False,
        "has_input_password": False,
    }
    repo_client.save_evidence(puppet_evidence)

    puppet_evidence = {
        "uuid": str(uuid.uuid4()),
        "parent": parent,
        "keywords": ",".join(["drug", "porn"]),
        "source": "website",
        "step": 2,
        "total_steps": 2,
        "url": "https://www.facebookcorewwwi.onion/",
        "title": "",
        "urls_found": [],
        "urls_queryable": [],
        "keywords_found": [],
        "has_form": False,
        "has_input_password": False,
    }
    repo_client.save_evidence(puppet_evidence)
    evidences = repo_client.get_evidences(1)
    assert 1 == len(evidences)
