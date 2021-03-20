import logging
import sys

class AuthenticationMiddleware(object):
    def __init__(self, app):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.app = app
        self.logger = logger
    
    def __call__(self, environ, start_response):
        self.logger.info('passed for '+str(start_response))
        return self.app(environ, start_response)
        