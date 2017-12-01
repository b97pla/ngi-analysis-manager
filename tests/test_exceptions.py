
import unittest
from ngi_analysis_manager.exceptions import exceptions


class TestProjectNotFoundError(unittest.TestCase):

    def test_project_name(self):
        project_name = "this-is-a-project-name"
        exception = exceptions.ProjectNotFoundError(project_name)
        self.assertGreaterEqual(str(exception).find(project_name), 0)

    def test_message(self):
        project_name = "this-is-a-project-name"
        message = "this-is-a-message"
        exception = exceptions.ProjectNotFoundError(project_name, message)
        self.assertGreaterEqual(str(exception).find(message), 0)
