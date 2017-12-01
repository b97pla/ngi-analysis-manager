
import unittest
from ngi_analysis_manager.connectors.base_connector import BaseConnector


class TestBaseConnector(unittest.TestCase):

    def test_not_implemented_error(self):
        base_connector = BaseConnector()
        # calling a method in the BaseConnector class should raise an exception
        with self.assertRaises(NotImplementedError) as obs_exception:
            base_connector.get_project("this-is-a-project-name")
        # the exception message should be informative
        self.assertGreaterEqual(str(obs_exception.exception).find("get_project"), 0)
        self.assertTrue(
            str(obs_exception.exception).endswith(
                "{}.".format(type(base_connector))
            ))
