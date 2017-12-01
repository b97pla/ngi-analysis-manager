
import json
from ngi_analysis_manager.connectors.base_connector import BaseConnector
from ngi_analysis_manager.exceptions.exceptions import ProjectNotFoundError


class JSONConnector(BaseConnector):

    def __init__(self, jsonfile, mode="r"):
        self.jsonfile = jsonfile
        self.mode = mode
        self.handle = None
        self.json_obj = None

    def open(self):
        """
        Open method for connector.

        If mode is to read, parse the contents into the JSON object.
        If mode is to write, this does nothing

        :return: None
        """
        # if write-mode, just initialize the internal object and return
        if self.mode == "w":
            self.json_obj = dict()
            return

        with open(self.jsonfile, self.mode) as jsonh:
            self.json_obj = json.load(jsonh)

    def close(self):
        """
        Close method for connector.

        This does nothing as all file handles should already be closed.

        :return: None
        """
        pass

    def commit(self):
        """
        Persist changes made to the object to the underlying file.

        If mode is read, this does nothing

        :return: None
        """
        if self.mode != "w":
            return None

        with open(self.jsonfile, "w") as jsonh:
            json.dump(self.json_obj, jsonh)

    def get_project(self, project_name):
        """
        Lookup a project and return the project name as it is represented in the JSON structure

        Raises ProjectNotFoundError if project is not found.

        :param project_name:
        :return: project name
        """
        if project_name not in self.json_obj.get("projects", {}):
            raise ProjectNotFoundError(project_name)

        return project_name
