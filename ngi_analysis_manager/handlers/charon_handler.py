from ngi_analysis_manager.models import charon_models


class CharonModelHandler:

    @staticmethod
    def project_from_json(json_obj):
        return charon_models.Project.from_json(json_obj)

    @staticmethod
    def sample_from_json(json_obj):
        return charon_models.Sample.from_json(json_obj)
