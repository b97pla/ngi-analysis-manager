
class NGIAnalysisManagerError(Exception):
    """
    Base class for user-defined exceptions.
    """
    def __init__(self, details, message=None):
        self.message = "{}{}".format(
            details,
            ": {}".format(message) if message is not None else "")


class ProjectNotFoundError(NGIAnalysisManagerError):
    """
    Exception that will be raised when a requested project id could not be found in a context

    Attributes:
        project_name -- the project name that could not be found
        message -- optional, additional information describing the exception circumstances
    """

    def __init__(self, project_name, message=None):
        super(ProjectNotFoundError, self).__init__(
            "Project '{}' could not be found".format(project_name),
            message)
        self.project_name = project_name


class ExpectedTypeNotMatchedError(NGIAnalysisManagerError):
    """
    Exception that will be raised when an unexpected object type was encountered

    Attributes:
        expected_type -- the expected type
        observed_type -- the observed type
        message -- optional, additional information describing the exception circumstances
    """

    def __init__(self, expected_type, observed_type, message=None):
        super(ExpectedTypeNotMatchedError, self).__init__(
            "Expected type {} but {} was observed".format(
                expected_type.__name__,
                observed_type.__name__),
            message)
        self.expected_type = expected_type
        self.observed_type = observed_type


class AttributeMissingError(NGIAnalysisManagerError):
    """
    Exception that will be raised when an attribute that is not present on an object is accessed

    Attributes:
        missing_attribute -- the name of the missing attribute
        accessed_object -- the object that was poked
        message -- optional, additional information describing the exception circumstances
    """

    def __init__(self, missing_attribute, accessed_object, message=None):
        super(AttributeMissingError, self).__init__(
            "Attribute with name {} not present on object".format(
                missing_attribute,
                str(accessed_object)),
            message)
        self.missing_attribute = missing_attribute
        self.accessed_object = accessed_object


class GenderNotRecognizedError(NGIAnalysisManagerError):
    """
    Exception that will be raised when a gender string could not be mapped to an object

    Attributes:
        gender_string -- the string that could not be mapped
        message -- optional, additional information describing the exception circumstances
    """

    def __init__(self, gender_string, message=None):
        super(GenderNotRecognizedError, self).__init__(
            "A gender object matching the string '{}' could not be created".format(gender_string),
            message)
        self.gender_string = gender_string


class SampleTypeNotRecognizedError(NGIAnalysisManagerError):
    """
    Exception that will be raised when a sample type string could not be mapped to an object

    Attributes:
        sample_type_string -- the string that could not be mapped
        message -- optional, additional information describing the exception circumstances
    """

    def __init__(self, sample_type, message=None):
        super(SampleTypeNotRecognizedError, self).__init__(
            "A sample type object matching the string '{}' could not be created".format(sample_type),
            message)
        self.sample_type = sample_type
