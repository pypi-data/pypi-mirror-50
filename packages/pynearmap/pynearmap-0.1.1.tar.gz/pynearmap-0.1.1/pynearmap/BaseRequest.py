from .Config.Auth import auth
import abc

import requests

class BaseRequest(abc.ABC):
    '''
    Request class responsible for handling API calls to nearmap
    '''
    api_key = auth.get("API_KEY")
    base_url = auth.get("BASE_URL")
    base_uri = None  # eg tiles/v3/surveys

    def __init__(self):
        self.base_request_url = self.base_url + self.base_uri
        self.queries = {}

    def set_params(self, **kwargs):
        self.params = kwargs

    def set_uri(self, uri: str):
        self.base_request_url = self.base_url + self.base_uri + uri
        return self

    def call(self):
        self.queries.update({
            "apiKey": self.api_key
        })

        # remove empty key
        params = {key: value for key, value in self.queries.items() if value is not None}

        return requests.get(self.base_request_url, params=params)
