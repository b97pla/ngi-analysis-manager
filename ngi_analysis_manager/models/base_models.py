from ngi_analysis_manager.exceptions.exceptions import \
    ExpectedTypeNotMatchedError, GenderNotRecognizedError, SampleTypeNotRecognizedError


class BaseObject:

    @staticmethod
    def add_attribute_with_type(current_attribute, attribute_value, attribute_type):
        """
        Append an attribute to an attribute list and check the type in the process.
        Will throw a ExpectedTypeNotMatchedError if the expected type does not match the received type.

        :param current_attribute: list attribute to append the value to
        :param attribute_value: The value to append
        :param attribute_type: The expected type of the attribute
        :return: None
        """
        if not isinstance(attribute_value, attribute_type):
            raise ExpectedTypeNotMatchedError(attribute_type, type(attribute_value))

        current_attribute.append(attribute_value)
        return current_attribute

    def to_json(self):
        """
        A default to_json method that follows a few simple rules:

        1. A dict is returned
        2. If an attribute's value is None or if it is an empty list, it is skipped
        3. Attributes that are of list type are added as a dict with the attribute name as key.
            The list is assumed to contain BaseObjects and it is therefore iterated over, calling
            each objects to_json method and update the dict with the result.
        3. Attributes of BaseObject type update the dict with the return value of that object's to_json method
        5. Other attribute values are just added as they are with the name of the attribute as key

        Any subclass can override this implementation

        :return: A dict constructed from the rules above
        """
        # first, create the json object
        json_obj = {}

        # next, get the attributes
        for attribute_name in self.__dict__:
            attribute_val = getattr(self, attribute_name)
            if type(attribute_val) is list:
                if len(attribute_val) > 0:
                    json_obj[attribute_name] = {}
                    for list_object in attribute_val:
                        json_obj[attribute_name].update(list_object.to_json())
            elif isinstance(attribute_val, BaseObject):
                json_obj.update(attribute_val.to_json())
            elif attribute_val is not None:
                json_obj[attribute_name] = attribute_val

        return json_obj


class Project(BaseObject):

    def __init__(self, project_name):
        self.project_name = project_name
        self.project_samples = []

    def add_project_sample(self, project_sample):
        self.add_attribute_with_type(self.project_samples, project_sample, Sample)

    @staticmethod
    def from_json(json_obj):
        project_name = json_obj.get("project_name")
        project_obj = Project(project_name)
        for sample_json in json_obj.get("project_samples", {}).values():
            sample_obj = Sample.from_json(sample_json)
            project_obj.add_project_sample(sample_obj)
        return project_obj

    def to_json(self):
        return {self.project_name: super(Project, self).to_json()}


class Sample(BaseObject):

    def __init__(self, sample_name, sample_gender=None, sample_type=None):
        self.sample_name = sample_name
        self.sample_gender = \
            self.add_attribute_with_type(
                [], sample_gender, SampleGender).pop() if sample_gender is not None else None
        self.sample_type = \
            self.add_attribute_with_type(
                [], sample_type, SampleType).pop() if sample_type is not None else None
        self.sample_relations = []
        self.sample_libraries = []

    def add_sample_library(self, sample_library):
        self.add_attribute_with_type(self.sample_libraries, sample_library, Library)

    def add_sample_relation(self, sample_relation):
        self.add_attribute_with_type(self.sample_relations, sample_relation, SampleRelation)

    @staticmethod
    def from_json(json_obj):
        sample_name = json_obj.get("sample_name")
        sample_gender = SampleGender.from_json(json_obj)
        sample_type = SampleType.from_json(json_obj)
        sample_obj = Sample(sample_name, sample_gender=sample_gender, sample_type=sample_type)
        for library_json in json_obj.get("sample_libraries", {}).values():
            library_obj = Library.from_json(library_json)
            sample_obj.add_sample_library(library_obj)
        return sample_obj

    def to_json(self):
        return {self.sample_name: super(Sample, self).to_json()}


class SampleRelation(BaseObject):

    def __init__(self, sample_a, sample_b, sample_relation_type):
        self.sample_a = self.add_attribute_with_type([], sample_a, Sample).pop()
        self.sample_b = self.add_attribute_with_type([], sample_b, Sample).pop()
        self.sample_relation_type = self.add_attribute_with_type(
            [], sample_relation_type, SampleRelationType).pop()


class Library(BaseObject):

    def __init__(self, library_name):
        self.library_name = library_name
        self.library_sequencing_runs = []

    def add_library_sequencing_run(self, library_sequencing_run):
        self.add_attribute_with_type(self.library_sequencing_runs, library_sequencing_run, SequencingRun)

    @staticmethod
    def from_json(json_obj):
        library_name = json_obj.get("library_name")
        library_obj = Library(library_name)
        for sequencing_run_json in json_obj.get("library_sequencing_runs", {}).values():
            sequencing_run_obj = SequencingRun.from_json(sequencing_run_json)
            library_obj.add_library_sequencing_run(sequencing_run_obj)
        return library_obj

    def to_json(self):
        return {self.library_name: super(Library, self).to_json()}


class SequencingRun(BaseObject):

    def __init__(self, sequencing_run_name):
        self.sequencing_run_name = sequencing_run_name
        self.sequencing_run_lanes = []

    def add_sequencing_run_lane(self, sequencing_run_lane):
        self.add_attribute_with_type(self.sequencing_run_lanes, sequencing_run_lane, SequencingRunLane)

    @staticmethod
    def from_json(json_obj):
        sequencing_run_name = json_obj.get("sequencing_run_name")
        sequencing_run_obj = SequencingRun(sequencing_run_name)
        for lane_json in json_obj.get("sequencing_run_lanes", {}).values():
            lane_obj = SequencingRunLane.from_json(lane_json)
            sequencing_run_obj.add_sequencing_run_lane(lane_obj)
        return sequencing_run_obj

    def to_json(self):
        return {self.sequencing_run_name: super(SequencingRun, self).to_json()}


class SequencingRunLane(BaseObject):

    def __init__(self, lane_num):
        self.lane_num = lane_num
        self.lane_barcodes = []

    def add_lane_barcode(self, lane_barcode):
        self.add_attribute_with_type(self.lane_barcodes, lane_barcode, LaneBarcode)

    @staticmethod
    def from_json(json_obj):
        lane_num = json_obj.get("lane_num")
        lane_obj = SequencingRunLane(lane_num)
        for barcode_json in json_obj.get("lane_barcodes", {}).values():
            barcode_obj = LaneBarcode.from_json(barcode_json)
            lane_obj.add_lane_barcode(barcode_obj)
        return lane_obj

    def to_json(self):
        return {self.lane_num: super(SequencingRunLane, self).to_json()}


class LaneBarcode(BaseObject):

    def __init__(self, barcode_seq):
        self.barcode_sequence = self.add_attribute_with_type([], barcode_seq, str).pop()

    @staticmethod
    def from_json(json_obj):
        barcode_seq = json_obj.get("barcode_sequence")
        barcode_obj = LaneBarcode(barcode_seq)
        return barcode_obj

    def to_json(self):
        return {self.barcode_sequence: super(LaneBarcode, self).to_json()}


class SampleGender(BaseObject):

    @staticmethod
    def create_instance(sample_gender):
        for cls in SampleGender.__subclasses__():
            if sample_gender.lower() in cls.DESCRIPTION:
                return cls()
        raise GenderNotRecognizedError(sample_gender)

    @staticmethod
    def from_json(json_obj):
        sample_gender = json_obj.get("sample_gender")
        return SampleGender.create_instance(sample_gender) if sample_gender is not None else None

    def to_json(self):
        return {"sample_gender": self.DESCRIPTION[0]}


class SampleGenderUnknown(SampleGender):
    DESCRIPTION = ["unknown"]


class SampleGenderFemale(SampleGender):
    DESCRIPTION = ["female", "f"]


class SampleGenderMale(SampleGender):
    DESCRIPTION = ["male", "m"]


class SampleType(BaseObject):

    @staticmethod
    def create_instance(sample_type):
        for cls in SampleType.__subclasses__():
            if sample_type.lower() in cls.DESCRIPTION:
                return cls()
        raise SampleTypeNotRecognizedError(sample_type)

    @staticmethod
    def from_json(json_obj):
        sample_type = json_obj.get("sample_type")
        return SampleType.create_instance(sample_type) if sample_type is not None else None

    def to_json(self):
        return {"sample_type": self.DESCRIPTION[0]}


class SampleTypeNormal(SampleType):
    DESCRIPTION = ["normal", "n"]


class SampleTypeTumor(SampleType):
    DESCRIPTION = ["tumor", "t"]


class SampleRelationType(BaseObject):
    pass


class RelationTypePaired(SampleRelationType):
    pass


class RelationTypeSibling(SampleRelationType):
    pass


class RelationTypeParent(SampleRelationType):
    pass
