import logging

import requests
from functools import wraps
import requests,time
from flask import request
from cachetools import cached, TTLCache

logging.getLogger().setLevel(logging.INFO)

JWT_API_URL= 'http://localhost:5002/validate_token'
cache = TTLCache(maxsize=1000, ttl=60)


class JWTClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.maxsize = 100
        pass

    def jwt_required(self,func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            jwt_token = request.headers.get('Authorization').split(' ')[1]
            user_id = self.validate_jwt(jwt_token)
            validation_time = time.time() - start_time
            if not user_id:
                return 'Invalid JWT token', 401
            function_response= func(user_id, *args, **kwargs)
            execution_time = time.time() - start_time
            logging.info(f'Validation time: {validation_time:.3f} seconds')
            logging.info(f'Execution time: {execution_time:.3f} seconds')
            return function_response

        return decorated_function

    @cached(cache)
    def validate_jwt(self,jwt_token):
        try:
            start_time = time.time()
            headers = {'content-type': 'application/json'}
            response = self.session.post(JWT_API_URL, params={'token': jwt_token}, headers=headers)
            validation_time = time.time() - start_time
            logging.info(f'Validation time: {validation_time:.3f} seconds')
            if response.status_code == 201:
                return response.json()['message']
            else:
                return None
        except requests.exceptions.RequestException:
            return None


jwt_client=JWTClient()



