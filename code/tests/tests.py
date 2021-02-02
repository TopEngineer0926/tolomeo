import unittest
from unittest import result
import requests
from http import client
import logging
import sys
import json

class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return super().setUp()

    def tearDown(self) -> None:
        self.logger.handlers[0].flush()
        return super().tearDown()

    ## makee sure it's working
    def test_true(self):
        a = True
        assert True == a, "Must Be true"
    
    def test_get_home(self):
        conn = client.HTTPConnection('localhost', 5000)
        conn.request('GET','/') 
        response = conn.getresponse()
        # self.logger.info(response.getcode())
        # self.logger.info(response.read().decode().strip())
        assert response.getcode() == 200

    def test_create_new_user(self):
        headers = {'Content-type': 'application/json'}
        json_data = json.dumps({'email': 'pippo@email.com'})
        conn = client.HTTPConnection('localhost', 5000)
        conn.request('POST','/users', json_data, headers) 
        response = conn.getresponse()
        body = response.read().decode().strip()
        data = json.loads(body)
        assert response.getcode() == 200
        assert data['email'] == 'pippo@email.com'

        conn.request('GET','/users/pippo@email.com') 
        response = conn.getresponse()
        body = response.read().decode().strip()
        data = json.loads(body)
        assert len(data) > 0
        assert response.getcode() == 200

        conn.request('DELETE','/users/pippo@email.com') 
        response = conn.getresponse()
        body = response.read().decode().strip()
        self.logger.info(body)
        assert response.getcode() == 200





if __name__ == "__main__":
    unittest.main()
    print('tested everything')