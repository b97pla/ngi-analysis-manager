
class NGIAnalysisManagerError(Exception):
    """
    Base class for user-defined exceptions.
    """
    pass


class ProjectNotFoundError(NGIAnalysisManagerError):
    """
    Exception that will be raised when a requested project id could not be found in a context

    Attributes:
        project_name -- the project name that could not be found
        message -- optional, additional information describing the exception circumstances
    """

    def __init__(self, project_name, message=None):
        self.project_name = project_name
        self.message = str(
            "Project '{}' could not be found{}".format(
                self.project_name,
                ": {}".format(message) if message is not None else ""
            ))
