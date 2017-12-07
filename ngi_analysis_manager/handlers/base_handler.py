from ngi_analysis_manager.models import base_models


class BaseModelHandler:

    @staticmethod
    def project_from_json(json_obj):
        return base_models.Project.from_json(json_obj)

    @staticmethod
    def sample_from_json(json_obj):
        return base_models.Sample.from_json(json_obj)

    @staticmethod
    def library_from_json(json_obj):
        return base_models.Library.from_json(json_obj)

    @staticmethod
    def sequencing_run_from_json(json_obj):
        return base_models.SequencingRun.from_json(json_obj)
