import mock
import unittest
from ngi_analysis_manager.exceptions.exceptions import ExpectedTypeNotMatchedError, TypeNotRecognizedError
from ngi_analysis_manager.models import base_models
import constants


class TestBaseObject(unittest.TestCase):

    def test_add_attribute_with_type(self):
        str_example = "this-is-a-str"
        self.assertListEqual(
            [str_example],
            base_models.BaseModel.add_attribute_with_type([], str_example, str))
        self.assertListEqual(
            [str_example, str_example],
            base_models.BaseModel.add_attribute_with_type([str_example], str_example, object))
        with self.assertRaises(ExpectedTypeNotMatchedError):
            base_models.BaseModel.add_attribute_with_type([], str_example, base_models.BaseModel)

    def test_to_json(self):
        base_obj = base_models.BaseModel()
        expected_absent = {
            "absent-key-1": None,
            "absent-key-2": []
        }
        mocked_json_response = {"mocked-json-response-key": "mocked-json-response-value"}
        base_obj_listed = base_models.BaseModel()
        base_obj_listed.to_json = mock.MagicMock(
            return_value=mocked_json_response)
        expected_present = {
            "present-key-1": "this-is-a-value-1",
            "present-key-2": [base_obj_listed],
            "present-key-3": {},
            "present-key-4": 123
        }
        for key, value in {**expected_absent, **expected_present}.items():
            setattr(base_obj, key, value)
        observed_json = base_obj.to_json()
        self.assertEqual(type(observed_json), dict)
        self.assertListEqual(list(observed_json.keys()), list(expected_present.keys()))
        for key, value in expected_present.items():
            if type(value) is list:
                self.assertDictEqual(observed_json[key], mocked_json_response)
            else:
                self.assertEqual(observed_json[key], expected_present[key])


class TestProject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.base_project = base_models.Project("this-is-a--project")

    def test_add_sample(self):

        # a non-sample type should raise an error
        with self.assertRaises(ExpectedTypeNotMatchedError) as err:
            self.base_project.add_project_sample("this-is-not-a-sample")

        expected_sample = base_models.Sample("this-is-a-base-sample")
        self.base_project.add_project_sample(expected_sample)
        self.assertListEqual([expected_sample], self.base_project.project_samples)

    def test_from_to_json(self):
        project_obj = base_models.Project.from_json(list(constants.PROJECT_JSON_OBJ.values()).pop())
        self.assertDictEqual(project_obj.to_json(), constants.PROJECT_JSON_OBJ)


class TestSample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


class TestSampleType(unittest.TestCase):

    def test_from_json(self):
        self.assertEqual(
            type(base_models.SampleType.from_json({"sample_type": "normal"})),
            base_models.SampleTypeNormal)
        self.assertEqual(
            type(base_models.SampleType.from_json({"sample_type": "tumor"})),
            base_models.SampleTypeTumor)
        self.assertIsNone(base_models.SampleType.from_json({}))
        with self.assertRaises(TypeNotRecognizedError):
            base_models.SampleType.from_json({"sample_type": "this-is-not-a-sample-type"})


class TestSampleRelation(unittest.TestCase):

    def setUp(self):
        self.base_sample_a = base_models.Sample("this-is-a-base-sample-a")
        self.base_sample_b = base_models.Sample("this-is-a-base-sample-b")
        self.base_sample_relation = base_models.RelationTypePaired()
