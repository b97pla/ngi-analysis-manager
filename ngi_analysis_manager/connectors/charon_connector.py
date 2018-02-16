
import json
import requests
from ngi_analysis_manager.connectors.base_connector import BaseConnector
from ngi_analysis_manager.exceptions.exceptions import NGIAnalysisManagerError
from ngi_analysis_manager.handlers.charon_handler import CharonModelHandler


class CharonResponseError(NGIAnalysisManagerError):
    def __init__(self, status_code, response_text, message=None):
        super(CharonResponseError, self).__init__(
            "Charon responded with status code {} and message {}".format(
                status_code,
                response_text
            ),
            message
        )


class CharonConnector(BaseConnector):

    API_VERSION = "v1"

    def __init__(self, base_url, api_token, model_handler=None, **kwargs):
        super(CharonConnector, self).__init__(**kwargs)
        self.base_url = base_url
        self.api_token = api_token
        self.model_handler = model_handler if model_handler is not None else CharonModelHandler()
        self.api_url = "{}/api/{}/".format(self.base_url, CharonConnector.API_VERSION)
        self.headers = {"X-Charon-API-token": self.api_token}
        self.session = None
        self.versions = None

    def url(self, endpoint):
        if type(endpoint) is list:
            endpoint = "/".join(endpoint)
        return "{}{}".format(self.api_url, endpoint)

    @staticmethod
    def handle_repsonse(response):
        if response.status_code != requests.codes.ok:
            raise CharonResponseError(response.status_code, response.text)
        return response.json()

    def open(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.versions = CharonConnector.handle_repsonse(
            self.session.get(self.url("version")))

    def get_project(self, project_name):
        endpoint = ["project", project_name]
        json_obj = self.handle_repsonse(self.session.get(self.url(endpoint)))
        project_obj = self.model_handler.project_from_json(json_obj)
        return project_obj

    def get_sample(self, project_name, sample_name):
        endpoint = ["sample", project_name, sample_name]
        json_obj = self.handle_repsonse(self.session.get(self.url(endpoint)))
        sample_obj = self.model_handler.sample_from_json(json_obj)
        return sample_obj
