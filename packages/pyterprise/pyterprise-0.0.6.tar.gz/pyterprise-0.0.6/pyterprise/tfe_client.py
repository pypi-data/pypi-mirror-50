import requests
import os
import logging as log
from .pyterprise_exceptions import UnauthorizedError, InternalServerError
from .organizations import Organziations
from .plans import Plans
from .teams import Teams
from .runs import Runs
from .variables import Variables
from .workspaces import Workspaces

"""
TODO: Test cases for for all requests using GET methods.
TODO: Refactor Posts and Puts to modify json payloads instead of creating dicts in methods.
TODO: Cover remainder of API methods.
"""

class Client(Organziations, Plans, Teams, Runs, Variables, Workspaces):
    log.basicConfig(
        level=log.CRITICAL
    )

    def __init__(self):
        self.payloads_dir = os.path.dirname(os.path.realpath(__file__)) + '/payloads/'

    def init(self, token, url):
        self.token = token
        self.url = url + '/api/v2/'
        self.headers = {
            'Content-Type': 'application/vnd.api+json',
            'Authorization': 'Bearer {}'.format(token)
        }

    def _tfe_api_get(self, url):
        response = requests.get(url=url, headers=self.headers)
        self._error_handler(response)
        return response.content

    def _error_handler(self, response):
        if response.status_code == 401 or response.status_code == 403:
            raise UnauthorizedError(
                message=response.content,
                errors=response.status_code
            )
        if response.status_code in range(500, 504):
            raise InternalServerError(
                message=response.content,
                errors=response.status_code
            )

        if response.status_code not in range(200, 202):
            log.warning('{}: {}'.format(response.url, response.status_code))
