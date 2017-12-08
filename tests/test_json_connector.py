
import filecmp
import json
import mock
import tempfile
import unittest
from ngi_analysis_manager.connectors.json_connector import JSONConnector
from ngi_analysis_manager.exceptions.exceptions import ProjectNotFoundError, ReadOnlyConnectorError
from ngi_analysis_manager.handlers.base_handler import BaseModelHandler
from ngi_analysis_manager.models.base_models import Project
import constants


class TestJSONConnector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _, cls.jsonfile_r = tempfile.mkstemp(".json", "test_json_connector_r_")
        _, cls.jsonfile_w = tempfile.mkstemp(".json", "test_json_connector_w_")
        cls.json_obj = {"projects": constants.PROJECT_JSON_OBJ}

        with open(cls.jsonfile_r, "w") as jsonh:
            json.dump(cls.json_obj, jsonh)

        with open(cls.jsonfile_w, "w") as jsonh:
            json.dump(cls.json_obj, jsonh)

    def setUp(self):
        self.model_handler = mock.MagicMock(spec=BaseModelHandler)
        self.json_connector_r = JSONConnector(self.jsonfile_r, model_handler=self.model_handler, read_only=True)
        self.json_connector_w = JSONConnector(self.jsonfile_w, model_handler=self.model_handler)

    def test_commit_read(self):
        with self.assertRaises(ReadOnlyConnectorError):
            self.json_connector_r.commit()

    def test_commit_write(self):
        self.json_connector_w.json_obj = self.json_obj
        self.json_connector_w.commit()
        self.assertTrue(filecmp.cmp(self.jsonfile_r, self.jsonfile_w, shallow=False))

    def test_open_read(self):
        self.json_connector_r.open()
        self.assertDictEqual(self.json_connector_r.json_obj, self.json_obj)

    def test_get_project(self):
        self.json_connector_r.open()
        project_name = list(self.json_obj["projects"].keys()).pop()
        # assert that a call is made to the model handler
        self.json_connector_r.get_project(project_name)
        self.model_handler.project_from_json.assert_called_once()
        # assert that an unknown name raises an exception
        with self.assertRaises(ProjectNotFoundError):
            self.json_connector_r.get_project("this-is-not-a-valid-project")

    def test_add_or_update_project(self):
        project_name = "ZZ-9876"
        expected_json = {
            "projects": {
                project_name: {
                    "project_name": project_name,
                    "project_samples": {}
            }}}
        project_obj = mock.MagicMock(spec=Project)
        project_obj.to_json = mock.MagicMock(return_value=expected_json["projects"])
        self.json_connector_w.open()
        self.json_connector_w.add_or_replace_project(project_obj)
        self.assertIn(
            project_name,
            self.json_connector_w.json_obj.get("projects", {}))
        self.assertDictEqual(
            expected_json["projects"][project_name],
            self.json_connector_w.json_obj["projects"][project_name])
