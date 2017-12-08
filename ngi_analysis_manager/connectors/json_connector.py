
import json
from ngi_analysis_manager.connectors.base_connector import BaseConnector
from ngi_analysis_manager.exceptions.exceptions import ProjectNotFoundError
from ngi_analysis_manager.handlers.base_handler import BaseModelHandler


class JSONConnector(BaseConnector):

    def __init__(self, jsonfile, model_handler=None, **kwargs):
        super(JSONConnector, self).__init__(**kwargs)
        self.jsonfile = jsonfile
        self.handle = None
        self.json_obj = None
        self.model_handler = model_handler if model_handler is not None else BaseModelHandler()

    def open(self):
        """
        Open method for connector.

        :return: None
        """
        with open(self.jsonfile, "r") as jsonh:
            self.json_obj = json.load(jsonh)

    def close(self):
        """
        Close method for connector.

        This does nothing as all file handles should already be closed.

        :return: None
        """
        pass

    @BaseConnector.mutator
    def commit(self):
        """
        Persist changes made to the object to the underlying file.

        If mode is read, this does nothing
        Raises ReadOnlyConnectorError if the connector is read-only.

        :return: None
        """
        with open(self.jsonfile, "w") as jsonh:
            json.dump(self.json_obj, jsonh)

    def get_project(self, project_name):
        """
        Lookup a project and return the project object as returned by this connector's model handler

        Raises ProjectNotFoundError if project is not found.

        :param project_name:
        :return: a Project object modelling the project according to this connector's model handler
        """
        if project_name not in self.json_obj.get("projects", {}):
            raise ProjectNotFoundError(project_name)

        return self.model_handler.project_from_json(self.json_obj["projects"][project_name])

    @BaseConnector.mutator
    def add_or_replace_project(self, project_obj):
        """
        Add or replace an existing project known to this connector.

        Note that no changes will be written until the commit method is called.
        Raises ReadOnlyConnectorError if the connector is read-only.

        :param project_obj: A Project object representing the project
        :return: None
        """
        self.json_obj.get("projects", {}).update(project_obj.to_json())
