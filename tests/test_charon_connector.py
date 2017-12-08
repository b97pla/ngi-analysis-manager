import mock
import unittest
from ngi_analysis_manager.connectors.charon_connector import CharonConnector, CharonResponseError


class TestCharonConnector(unittest.TestCase):

    BASE_URL = "this-is-the-base-url"
    API_TOKEN = "this-is-the-api-token"

    def setUp(self):
        self.charon_connector_r = CharonConnector(self.BASE_URL, self.API_TOKEN, read_only=True)

    def test_url(self):
        endpoint = "this-is-endpoint"
        url = self.charon_connector_r.url(endpoint)
        self.assertTrue(url.startswith(self.BASE_URL))
        self.assertTrue(url.split("/")[-1] == endpoint)
        endpoint = ["this", "is", "endpoint"]
        url = self.charon_connector_r.url(endpoint)
        self.assertListEqual(url.split("/")[-3:], endpoint)

    def test_handle_response(self):
        expected_json_response = {"this-is-the": "json-response"}
        response = mock.MagicMock()
        response.status_code = 200
        response.json = mock.MagicMock(return_value=expected_json_response)
        self.assertDictEqual(self.charon_connector_r.handle_repsonse(response), expected_json_response)
        response.status_code = 400
        with self.assertRaises(CharonResponseError):
            self.charon_connector_r.handle_repsonse(response)

    def test_get_project(self):
        connector = CharonConnector(
            "https://charon.scilifelab.se", "39ffbffa6b7a4ae0aca15400e5709562", read_only=True)
        connector.open()
        connector.get_project("MH-0336")

    def test_get_sample(self):
        connector = CharonConnector(
            "https://charon.scilifelab.se", "39ffbffa6b7a4ae0aca15400e5709562", read_only=True)
        connector.open()
        connector.get_sample("MH-0336", "Sf12-t1-l2-dr")
