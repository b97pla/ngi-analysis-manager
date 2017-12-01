
import filecmp
import json
import mock
import tempfile
import unittest
from ngi_analysis_manager.connectors.json_connector import JSONConnector
from ngi_analysis_manager.exceptions.exceptions import ProjectNotFoundError


class TestJSONConnector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _, cls.jsonfile_r = tempfile.mkstemp(".json", "test_json_connector_r_")
        _, cls.jsonfile_w = tempfile.mkstemp(".json", "test_json_connector_w_")
        cls.json_obj = {"projects": {
            "AA-0123": {
                "samples": {
                    "AA-0123-Sample_1": [],
                    "AA-0123-Sample_2": []
                }}}}
        with open(cls.jsonfile_r, "w") as jsonh:
            json.dump(cls.json_obj, jsonh)

    def setUp(self):
        self.json_connector_r = JSONConnector(self.jsonfile_r, "r")
        self.json_connector_w = JSONConnector(self.jsonfile_w, "w")

    def test_commit_read(self):
        with mock.patch('builtins.open') as mock_open:
            self.json_connector_r.commit()
            mock_open.assert_not_called()

    def test_commit_write(self):
        self.json_connector_w.json_obj = self.json_obj
        self.json_connector_w.commit()
        self.assertTrue(filecmp.cmp(self.jsonfile_r, self.jsonfile_w, shallow=False))

    def test_open_read(self):
        self.json_connector_r.open()
        self.assertDictEqual(self.json_connector_r.json_obj, self.json_obj)

    def test_open_write(self):
        with mock.patch('builtins.open') as mock_open:
            self.json_connector_w.open()
            mock_open.assert_not_called()

    def test_get_project(self):
        self.json_connector_r.open()
        project_name = list(self.json_obj["projects"].keys()).pop()
        # assert that a known name is returned
        self.assertEqual(self.json_connector_r.get_project(project_name), project_name)
        # assert that an unknown name raises an exception
        with self.assertRaises(ProjectNotFoundError):
            self.json_connector_r.get_project("this-is-not-a-valid-project")
