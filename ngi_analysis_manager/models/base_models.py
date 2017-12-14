from ngi_analysis_manager.exceptions.exceptions import \
    ExpectedTypeNotMatchedError, GenderNotRecognizedError, TypeNotRecognizedError


class BaseModel:

    @classmethod
    def create_instance(cls, description):
        if description is None:
            return None
        # print("{} {}".format(cls, cls.__subclasses__()))
        for subcls in cls.__subclasses__():
            if description.lower() in subcls.DESCRIPTION:
                return subcls(description)
        raise TypeNotRecognizedError(description, message=cls.__name__)

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
        3. Attributes of BaseModel type update the dict with the return value of that object's to_json method
        5. Other attribute values are just added as they are with the name of the attribute as key

        Any subclass can override this implementation

        :return: A dict constructed from the rules above
        """
        # first, create the json object
        json_obj = {}

        # initialize the attribute_name_translation to a proper dict if needed
        attribute_name_translation = getattr(self, "attribute_name_translation", dict())

        # next, get the attributes
        for attribute_name in self.__dict__:
            attribute_val = getattr(self, attribute_name)
            # translate the attribute name if such a translation exists
            attribute_name = attribute_name_translation.get(attribute_name, attribute_name)
            if type(attribute_val) is list:
                if len(attribute_val) > 0:
                    json_obj[attribute_name] = {}
                    for list_object in attribute_val:
                        json_obj[attribute_name].update(list_object.to_json())
            elif isinstance(attribute_val, BaseModel):
                json_obj.update(attribute_val.to_json())
            elif attribute_val is not None:
                json_obj[attribute_name] = attribute_val

        return json_obj


class Project(BaseModel):

    def __init__(self, project_name):
        self.project_name = project_name
        self.project_status = None
        self.analysis_type = None
        self.sequencing_facility = None
        self.delivery_status = None
        self.project_samples = []

    def add_project_sample(self, project_sample):
        self.add_attribute_with_type(self.project_samples, project_sample, Sample)

    def set_status(self, status):
        self.project_status = self.add_attribute_with_type([], status, StatusModel).pop()

    def set_analysis_type(self, analysis_type):
        self.analysis_type = self.add_attribute_with_type([], analysis_type, AnalysisType).pop()

    def set_sequencing_facility(self, sequencing_facility):
        self.sequencing_facility = self.add_attribute_with_type([], sequencing_facility, SequencingFacility).pop()

    def set_delivery_status(self, delivery_status):
        self.delivery_status = self.add_attribute_with_type([], delivery_status, DeliveryStatus).pop()

    @classmethod
    def from_json(cls, json_obj):
        project_name = json_obj.get("project_name")
        project_obj = cls(project_name)
        for sample_json in json_obj.get("project_samples", {}).values():
            sample_obj = Sample.from_json(sample_json)
            project_obj.add_project_sample(sample_obj)
        return project_obj

    def to_json(self):
        return {self.project_name: super(Project, self).to_json()}


class Sample(BaseModel):

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

    @classmethod
    def from_json(cls, json_obj):
        sample_name = json_obj.get("sample_name")
        sample_gender = SampleGender.from_json(json_obj)
        sample_type = SampleType.from_json(json_obj)
        sample_obj = cls(sample_name, sample_gender=sample_gender, sample_type=sample_type)
        for library_json in json_obj.get("sample_libraries", {}).values():
            library_obj = Library.from_json(library_json)
            sample_obj.add_sample_library(library_obj)
        return sample_obj

    def to_json(self):
        return {self.sample_name: super(Sample, self).to_json()}


class SampleRelation(BaseModel):

    def __init__(self, sample_a, sample_b, sample_relation_type):
        self.sample_a = self.add_attribute_with_type([], sample_a, Sample).pop()
        self.sample_b = self.add_attribute_with_type([], sample_b, Sample).pop()
        self.sample_relation_type = self.add_attribute_with_type(
            [], sample_relation_type, SampleRelationType).pop()


class Library(BaseModel):

    def __init__(self, library_name):
        self.library_name = library_name
        self.library_sequencing_runs = []

    def add_library_sequencing_run(self, library_sequencing_run):
        self.add_attribute_with_type(self.library_sequencing_runs, library_sequencing_run, SequencingRun)

    @classmethod
    def from_json(cls, json_obj):
        library_name = json_obj.get("library_name")
        library_obj = cls(library_name)
        for sequencing_run_json in json_obj.get("library_sequencing_runs", {}).values():
            sequencing_run_obj = SequencingRun.from_json(sequencing_run_json)
            library_obj.add_library_sequencing_run(sequencing_run_obj)
        return library_obj

    def to_json(self):
        return {self.library_name: super(Library, self).to_json()}


class SequencingRun(BaseModel):

    def __init__(self, sequencing_run_name):
        self.sequencing_run_name = sequencing_run_name
        self.sequencing_run_lanes = []

    def add_sequencing_run_lane(self, sequencing_run_lane):
        self.add_attribute_with_type(self.sequencing_run_lanes, sequencing_run_lane, SequencingRunLane)

    @classmethod
    def from_json(cls, json_obj):
        sequencing_run_name = json_obj.get("sequencing_run_name")
        sequencing_run_obj = cls(sequencing_run_name)
        for lane_json in json_obj.get("sequencing_run_lanes", {}).values():
            lane_obj = SequencingRunLane.from_json(lane_json)
            sequencing_run_obj.add_sequencing_run_lane(lane_obj)
        return sequencing_run_obj

    def to_json(self):
        return {self.sequencing_run_name: super(SequencingRun, self).to_json()}


class SequencingRunLane(BaseModel):

    def __init__(self, lane_num):
        self.lane_num = lane_num
        self.lane_barcodes = []

    def add_lane_barcode(self, lane_barcode):
        self.add_attribute_with_type(self.lane_barcodes, lane_barcode, LaneBarcode)

    @classmethod
    def from_json(cls, json_obj):
        lane_num = json_obj.get("lane_num")
        lane_obj = cls(lane_num)
        for barcode_json in json_obj.get("lane_barcodes", {}).values():
            barcode_obj = LaneBarcode.from_json(barcode_json)
            lane_obj.add_lane_barcode(barcode_obj)
        return lane_obj

    def to_json(self):
        return {self.lane_num: super(SequencingRunLane, self).to_json()}


class LaneBarcode(BaseModel):

    def __init__(self, barcode_seq):
        self.barcode_sequence = self.add_attribute_with_type([], barcode_seq, str).pop()

    @classmethod
    def from_json(cls, json_obj):
        barcode_seq = json_obj.get("barcode_sequence")
        barcode_obj = cls(barcode_seq)
        return barcode_obj

    def to_json(self):
        return {self.barcode_sequence: super(LaneBarcode, self).to_json()}


class SampleGender(BaseModel):

    def __init__(self, sample_gender):
        self.sample_gender = sample_gender

    @classmethod
    def from_json(cls, json_obj):
        sample_gender = json_obj.get("sample_gender")
        return cls.create_instance(sample_gender)


class SampleGenderUnknown(SampleGender):
    DESCRIPTION = ["unknown"]


class SampleGenderFemale(SampleGender):
    DESCRIPTION = ["female", "f"]


class SampleGenderMale(SampleGender):
    DESCRIPTION = ["male", "m"]


class SampleType(BaseModel):

    def __init__(self, sample_type):
        self.sample_type = sample_type

    @classmethod
    def from_json(cls, json_obj):
        sample_type = json_obj.get("sample_type")
        return cls.create_instance(sample_type)


class SampleTypeNormal(SampleType):
    DESCRIPTION = ["normal", "n"]


class SampleTypeTumor(SampleType):
    DESCRIPTION = ["tumor", "t"]


class SampleRelationType(BaseModel):

    def __init__(self, sample_relation_type):
        self.sample_relation_type = sample_relation_type

    @classmethod
    def from_json(cls, json_obj):
        sample_relation_type = json_obj.get("sample_relation_type")
        return cls.create_instance(sample_relation_type)


class RelationTypePaired(SampleRelationType):
    DESCRIPTION = ["paired"]


class RelationTypeSibling(SampleRelationType):
    DESCRIPTION = ["sibling"]


class RelationTypeParent(SampleRelationType):
    DESCRIPTION = ["parent"]


class StatusModel(BaseModel):

    def __init__(self, status):
        self.status = status

    @classmethod
    def from_json(cls, json_obj):
        status = json_obj.get("status")
        return cls.create_instance(status)


class StatusClosed(StatusModel):
    DESCRIPTION = ["closed"]


class StatusOpen(StatusModel):
    DESCRIPTION = ["open"]


class StatusAborted(StatusModel):
    DESCRIPTION = ["aborted"]


class StatusFresh(StatusModel):
    DESCRIPTION = ["fresh"]


class StatusStale(StatusModel):
    DESCRIPTION = ["stale"]


class DeliveryStatus(BaseModel):

    def __init__(self, delivery_status):
        self.delivery_status = delivery_status

    @classmethod
    def from_json(cls, json_obj):
        delivery_status = json_obj.get("delivery_status")
        return cls.create_instance(delivery_status)


class DeliveryStatusNotDelivered(DeliveryStatus):
    DESCRIPTION = ["not delivered"]


class DeliveryStatusDelivered(DeliveryStatus):
    DESCRIPTION = ["delivered"]


class AnalysisType(BaseModel):

    def __init__(self, analysis_type):
        self.analysis_type = analysis_type

    @classmethod
    def from_json(cls, json_obj):
        analysis_type = json_obj.get("analysis_type")
        return cls.create_instance(analysis_type)


class AnalysisTypeWGS(AnalysisType):
    DESCRIPTION = ["whole_genome_reseq", "wgs"]


class AnalysisTypeRNASeq(AnalysisType):
    DESCRIPTION = ["rna_seq", "ngi_rna_seq"]


class SequencingFacility(BaseModel):

    def __init__(self, sequencing_facility):
        self.sequencing_facility = sequencing_facility

    @classmethod
    def from_json(cls, json_obj):
        sequencing_facility = json_obj.get("sequencing_facility")
        return cls.create_instance(sequencing_facility)


class SequencingFacilityNGIU(SequencingFacility):
    DESCRIPTION = ["ngi-u", "upps", "uppsala", "snpseq"]


class SequencingFacilityNGIS(SequencingFacility):
    DESCRIPTION = ["ngi-s", "sthlm", "stockholm"]


