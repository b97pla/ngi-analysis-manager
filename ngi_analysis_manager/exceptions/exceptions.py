
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


class TypeNotRecognizedError(NGIAnalysisManagerError):
    """
    Exception that will be raised when a type string could not be mapped to an object

    Attributes:
        type_string -- the string that could not be mapped
        message -- optional, additional information describing the exception circumstances
    """

    def __init__(self, type_string, message=None):
        super(TypeNotRecognizedError, self).__init__(
            "A type object matching the string '{}' could not be created".format(type_string),
            message)
        self.type_string = type_string


class ReadOnlyConnectorError(NGIAnalysisManagerError):
    """
    Exception that will be raised if changes are attempted on a read-only connector

    Attributes:
          connector_obj -- the read-only connector object where the exception was raised
          message -- optional, additional information describing the exception circumstances
    """

    def __init__(self, connector_object, message=None):
        super(ReadOnlyConnectorError, self).__init__(
            "The {} connector object was opened as read-only so no changes can be made".format(
                type(connector_object).__name__),
            message)
        self.connector_object = connector_object
