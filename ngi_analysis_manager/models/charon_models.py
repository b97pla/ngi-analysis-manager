
from ngi_analysis_manager.models import base_models


class Project(base_models.Project):

    attribute_name_translation = {
        "project_name": "projectid",
        "analysis_type": "best_practice_analysis",
    }

    @staticmethod
    def from_json(json_obj):
        # translate the keys in the json_obj to match the base model
        for base_key, charon_key in Project.attribute_name_translation.items():
            if charon_key in json_obj.keys():
                json_obj[base_key] = json_obj.pop(charon_key)
        project_name = json_obj.get("project_name")
        project_obj = Project(project_name)
        project_obj.set_status(StatusObject.from_json(json_obj))
        project_obj.set_analysis_type(AnalysisType.from_json(json_obj))
        project_obj.set_sequencing_facility(SequencingFacility.from_json(json_obj))
        project_obj.set_delivery_status(DeliveryStatus.from_json(json_obj))
        return project_obj

    def to_json(self):
        json_obj = super(Project, self).to_json()
        return list(json_obj.values()).pop()


class Sample(base_models.Sample):

    attribute_name_translation = {
        "sample_name": "sampleid"}

    @staticmethod
    def from_json(json_obj):
        sample_name = json_obj.get("sampleid")
        sample_obj = Sample(sample_name)
        return sample_obj

    def to_json(self):
        json_obj = super(Sample, self).to_json()
        return list(json_obj.values()).pop()


class StatusObject(base_models.StatusObject):
    pass


class AnalysisType(base_models.AnalysisType):
    pass


class SequencingFacility(base_models.SequencingFacility):
    pass


class DeliveryStatus(base_models.DeliveryStatus):
    pass
