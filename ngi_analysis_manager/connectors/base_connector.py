

class BaseConnector:

    def __init__(self):
        pass

    def _get_notimplementederror(self, method_name):
        return NotImplementedError("Method {} is not implemented by {}.".format(method_name, str(type(self))))

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

