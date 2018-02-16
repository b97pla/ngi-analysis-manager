import csv
import os
from ngi_analysis_manager.connectors.json_connector import JSONConnector
from ngi_analysis_manager.exceptions.exceptions import \
    SampleSheetNotFoundError, SampleSheetFormatNotRecognizedError
from ngi_analysis_manager.utils import utils


class FileSystemConnector(JSONConnector):

    POSSIBLE_SAMPLESHEET_NAMES = ["SampleSheet.csv"]

    def __init__(self, base_path, **kwargs):
        super(FileSystemConnector, self).__init__(
            os.path.join(base_path, "SampleSheet.json"),
            read_only=True,
            **{k: v for k, v in kwargs.items() if k != "read_only"})
        self.base_path = base_path
        self.runfolder_name = os.path.basename(self.base_path)
        self.samplesheet_path = None

    def _locate_samplesheet(self):
        for samplesheet_name in self.POSSIBLE_SAMPLESHEET_NAMES:
            path_to_check = os.path.join(self.base_path, samplesheet_name)
            if os.path.exists(path_to_check):
                return path_to_check
        raise SampleSheetNotFoundError(self.base_path)

    def _samplesheet_to_json(self, samplesheet_path):
        json_obj = {"projects": {}}
        with open(samplesheet_path) as fh:
            for line in fh:
                if line.startswith("[Data]"):
                    break
            csv_reader = csv.DictReader(fh, delimiter=",")
            rows = list(csv_reader)
        if len(rows) == 0:
            raise SampleSheetFormatNotRecognizedError(samplesheet_path, "the expected [Data] section was not found")
        try:
            for sample_row in rows:
                sample_name = sample_row["Sample_Name"]
                sample_id = sample_row["Sample_ID"]
                sample_project = sample_row["Sample_Project"]
                sample_lane = sample_row["Lane"]
                sample_barcode = sample_row["index"]
                sample_library = {}
                sample_description = sample_row["Description"]
                for key_value in sample_description.split(";"):
                    key, value = key_value.split(":")
                    sample_library[key.lower()] = value
                if "library_name" not in sample_library:
                    raise SampleSheetFormatNotRecognizedError(
                        samplesheet_path,
                        "the LIBRARY_NAME tag could not be parsed from the Description '{}'".format(
                            sample_description))
                tag_json = {
                    sample_project: {
                        "project_name": sample_project,
                        "project_samples": {
                            sample_name: {
                                "sample_name": sample_name,
                                "sample_id": sample_id,
                                "sample_libraries": {
                                    sample_library["library_name"]: {
                                        "library_name": sample_library["library_name"],
                                        "fragment_size": sample_library.get("fragment_size"),
                                        "fragment_lower": sample_library.get("fragment_lower"),
                                        "fragment_upper": sample_library.get("fragment_upper"),
                                        "library_sequencing_runs": {
                                            self.runfolder_name: {
                                                "sequencing_run_name": self.runfolder_name,
                                                "sequencing_run_lanes": {
                                                    sample_lane: {
                                                        "lane_num": sample_lane,
                                                        "lane_barcodes": {
                                                            sample_barcode: {
                                                                "barcode_sequence": sample_barcode
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                utils.dict_merge(json_obj["projects"], tag_json)
        except KeyError as ke:
            raise SampleSheetFormatNotRecognizedError(samplesheet_path, str(ke))
        return json_obj

    def open(self):
        self.samplesheet_path = self._locate_samplesheet()
        self.json_obj = self._samplesheet_to_json(self.samplesheet_path)


