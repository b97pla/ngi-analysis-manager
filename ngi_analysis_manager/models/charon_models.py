
from ngi_analysis_manager.models import base_models


class CharonObject(base_models.BaseObject):
    pass


class Project(CharonObject, base_models.Project):

    attribute_name_translation = {
        "project_name": "projectid",
        "analysis_type": "best_practice_analysis",
    }

    @classmethod
    def from_json(cls, json_obj):
        # translate the keys in the json_obj to match the base model
        for base_key, charon_key in cls.attribute_name_translation.items():
            if charon_key in json_obj.keys():
                json_obj[base_key] = json_obj.pop(charon_key)
        project_name = json_obj.get("project_name")
        project_obj = cls(project_name)
        project_obj.set_status(StatusObject.from_json(json_obj))
        project_obj.set_analysis_type(AnalysisType.from_json(json_obj))
        project_obj.set_sequencing_facility(SequencingFacility.from_json(json_obj))
        project_obj.set_delivery_status(DeliveryStatus.from_json(json_obj))
        return project_obj

    def to_json(self):
        json_obj = super(Project, self).to_json()
        return list(json_obj.values()).pop()


class Sample(CharonObject, base_models.Sample):

    attribute_name_translation = {
        "sample_name": "sampleid"}

    @classmethod
    def from_json(cls, json_obj):
        for base_key, charon_key in cls.attribute_name_translation.items():
            if charon_key in json_obj.keys():
                json_obj[base_key] = json_obj.pop(charon_key)
        sample_name = json_obj.get("sample_name")
        sample_obj = cls(sample_name)
        return sample_obj

    def to_json(self):
        json_obj = super(Sample, self).to_json()
        return list(json_obj.values()).pop()


class StatusObject(CharonObject, base_models.StatusObject):
    pass


class StatusClosed(StatusObject, base_models.StatusClosed):
    pass


class StatusOpen(StatusObject, base_models.StatusOpen):
    pass


class StatusAborted(StatusObject, base_models.StatusAborted):
    pass


class StatusStale(StatusObject, base_models.StatusAborted):
    pass


class StatusFresh(StatusObject, base_models.StatusAborted):
    pass


class AnalysisType(CharonObject, base_models.AnalysisType):
    pass


class AnalysisTypeWGS(AnalysisType, base_models.AnalysisTypeWGS):
    pass


class AnalysisTypeRNASeq(AnalysisType, base_models.AnalysisTypeRNASeq):
    pass


class SequencingFacility(CharonObject, base_models.SequencingFacility):
    pass


class SequencingFacilityNGIU(SequencingFacility, base_models.SequencingFacilityNGIU):
    pass


class SequencingFacilityNGIS(SequencingFacility, base_models.SequencingFacilityNGIS):
    pass


class DeliveryStatus(CharonObject, base_models.DeliveryStatus):
    pass


class DeliveryStatusNotDelivered(DeliveryStatus, base_models.DeliveryStatusNotDelivered):
    pass


class DeliveryStatusDelivered(DeliveryStatus, base_models.DeliveryStatusDelivered):
    pass

