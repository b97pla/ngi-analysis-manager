
from ngi_analysis_manager.exceptions.exceptions import ReadOnlyConnectorError


class BaseConnector:

    def __init__(self, read_only=False):
        self.read_only = read_only

    def _get_notimplementederror(self, method_name):
        return NotImplementedError("Method {} is not implemented by {}.".format(method_name, str(type(self))))

    @classmethod
    def mutator(cls, fun):
        """
        This is a decorator that can be added to all methods that will modify the connector's content.
        It will raise an exception if the connector is read-only.
        :return:
        """
        def wrapper(self, *args, **kwargs):
            if self.read_only:
                raise ReadOnlyConnectorError(self)
            return fun(self, *args, **kwargs)
        return wrapper

    def commit(self):
        """
        Commit the changes made.

        Should be implemented in subclasses.

        :return: None
        """
        raise self._get_notimplementederror("commit")

    def close(self):
        """
        Close the connection.

        Should be implemented in subclasses.

        :return: None
        """
        raise self._get_notimplementederror("close")

    def get_project(self, project_name):
        """
        Lookup a project name and return.

        Raises ProjectNotFoundError if project is not found.

        Should be implemented in subclasses.

        :param project_name: name of the project to fetch
        :return:
        """
        raise self._get_notimplementederror("get_project")

    def open(self):
        """
        Open the connection.

        Should be implemented in subclasses.

        :return: None
        """
        raise self._get_notimplementederror("open")

