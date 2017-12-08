
import unittest
from ngi_analysis_manager.exceptions import exceptions


class NGIAnalysisManagerError(unittest.TestCase):

    def test_details(self):
        details = "this-is-a-detail"
        exception = exceptions.NGIAnalysisManagerError(details)
        self.assertGreaterEqual(str(exception).find(details), 0)

    def test_message(self):
        details = "this-is-a-detail"
        message = "this-is-a-message"
        exception = exceptions.ProjectNotFoundError(details, message)
        self.assertGreaterEqual(str(exception).find(message), 0)
