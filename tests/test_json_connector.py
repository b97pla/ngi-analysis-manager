
import unittest
from ngi_analysis_manager.connectors.json_connector import JSONConnector


class TestJSONConnector(unittest.TestCase):

    def test_get_project(self):
        json_connector = JSONConnector("json-file")
        with self.assertRaises(NotImplementedError) as error:
            json_connector.get_project("this-is-a-project")
