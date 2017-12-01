
from ngi_analysis_manager.connectors.base_connector import BaseConnector


class JSONConnector(BaseConnector):

    def __init__(self, jsonfile):
        self.jsonfile = jsonfile
