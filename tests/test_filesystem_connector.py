import json
import mock
import os
import shutil
import tempfile
import unittest
from ngi_analysis_manager.connectors.filesystem_connector import FileSystemConnector
from ngi_analysis_manager.handlers.base_handler import BaseModelHandler
from ngi_analysis_manager.exceptions.exceptions import SampleSheetNotFoundError, SampleSheetFormatNotRecognizedError


class TestFileSystemConnector(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.samplesheet_dir = tempfile.mkdtemp(prefix="test_samplesheet_connector_")
        cls.samplesheet = os.path.join(cls.samplesheet_dir, "SampleSheet.csv")
        cls.samplesheet_json_sample = {
            "projects": {
                "AA-0001": {
                    "project_name": "AA-0001",
                    "project_samples": {
                        "AA-0001-Sample_2": {
                            "sample_name": "AA-0001-Sample_2",
                            "sample_id": "Sample_AA-0001-Sample_2",
                            "sample_libraries": {
                                "AA-0001-Sample_2_2-80988": {
                                    "library_name": "AA-0001-Sample_2_2-80988",
                                    "fragment_size": "364",
                                    "fragment_lower": "230",
                                    "fragment_upper": "730",
                                    "library_sequencing_runs": {
                                        os.path.basename(cls.samplesheet_dir): {
                                            "sequencing_run_name": os.path.basename(cls.samplesheet_dir),
                                            "sequencing_run_lanes": {
                                                "1": {
                                                    "lane_num": "1",
                                                    "lane_barcodes": {
                                                        "ATTCCT": {
                                                            "barcode_sequence": "ATTCCT"},
                                                        "TTAGGC": {
                                                            "barcode_sequence": "TTAGGC"}}},
                                                "2": {
                                                    "lane_num": "2",
                                                    "lane_barcodes": {
                                                        "ATTCCT": {
                                                            "barcode_sequence": "ATTCCT"}}}}}}}}}}},
                "BB-0002": {
                    "project_name": "BB-0002"},
                "CC-0003": {
                    "project_name": "CC-0003"},
                "DD-0004": {
                    "project_name": "DD-0004",
                    "project_samples": {
                        "DD-0004-Sample_1": {
                            "sample_name": "DD-0004-Sample_1",
                            "sample_id": "Sample_DD-0004-Sample_1"},
                        "DD-0004-Sample_2": {
                            "sample_name": "DD-0004-Sample_2",
                            "sample_id": "Sample_DD-0004-Sample_2"},
                        "DD-0004-Sample_3": {
                            "sample_name": "DD-0004-Sample_3",
                            "sample_id": "Sample_DD-0004-Sample_3"},
                        "DD-0004-Sample_4": {
                            "sample_name": "DD-0004-Sample_4",
                            "sample_id": "Sample_DD-0004-Sample_4"}}}}}
        cls.samplesheet_contents = """
[Header],,,,,,,,
IEMFileVersion,1,,,,,,,
Date,2017-11-17,,,,,,,
Workflow,Resequencing - HiSeqX,,,,,,,
Application,WGS re-seq,,,,,,,
Assay,TruSeq LT,,,,,,,
Description,<none>,,,,,,,
Chemistry,Default,,,,,,,
,,,,,,,,
[Reads],,,,,,,,
151,,,,,,,,
151,,,,,,,,
,,,,,,,,
[Settings],,,,,,,,
Adapter,,,,,,,,
Adapter Read 2,,,,,,,,
,,,,,,,,
[Data],,,,,,,,
Lane,Sample_ID,Sample_Name,Sample_Plate,Sample_Well,I7_Index_ID,index,Sample_Project,Description
1,Sample_AA-0001-Sample_1,AA-0001-Sample_1,,,,ACTGAT,AA-0001,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:AA-0001-Sample_1_2-80988
1,Sample_AA-0001-Sample_2,AA-0001-Sample_2,,,,ATTCCT,AA-0001,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:AA-0001-Sample_2_2-80988
1,Sample_AA-0001-Sample_1,AA-0001-Sample_1,,,,CGATGT,AA-0001,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:AA-0001-Sample_1_2-80988
1,Sample_AA-0001-Sample_2,AA-0001-Sample_2,,,,TTAGGC,AA-0001,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:AA-0001-Sample_2_2-80988
2,Sample_AA-0001-Sample_1,AA-0001-Sample_1,,,,ACTGAT,AA-0001,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:AA-0001-Sample_1_2-80988
2,Sample_AA-0001-Sample_2,AA-0001-Sample_2,,,,ATTCCT,AA-0001,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:AA-0001-Sample_2_2-80988
2,Sample_BB-0002-Sample_1,BB-0002-Sample_1,,,,CGATGT,BB-0002,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:BB-0002-Sample_1_2-80988
3,Sample_BB-0002-Sample_1,BB-0002-Sample_1,,,,CGATGT,BB-0002,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:BB-0002-Sample_1_2-80988
4,Sample_CC-0003-Sample_1,CC-0003-Sample_1,,,,,CC-0003,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:CC-0003-Sample_1_2-80988
5,Sample_DD-0004-Sample_1,DD-0004-Sample_1,,,,ACTGAT-ATTCCT,DD-0004,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:DD-0004-Sample_1_2-80988
6,Sample_DD-0004-Sample_2,DD-0004-Sample_2,,,,ACTGAT-ATTCCT,DD-0004,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:DD-0004-Sample_2_2-80988
7,Sample_DD-0004-Sample_3,DD-0004-Sample_3,,,,ACTGAT-ATTCCT,DD-0004,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:DD-0004-Sample_3_2-80988
8,Sample_DD-0004-Sample_4,DD-0004-Sample_4,,,,ACTGAT-ATTCCT,DD-0004,FRAGMENT_SIZE:364;FRAGMENT_LOWER:230;FRAGMENT_UPPER:730;LIBRARY_NAME:DD-0004-Sample_4_2-80988
"""
        cls._write_samplesheet(contents=cls.samplesheet_contents, samplesheet=cls.samplesheet)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.samplesheet_dir)

    @classmethod
    def _write_samplesheet(cls, contents=None, samplesheet=None):
        if samplesheet is None:
            _, samplesheet = tempfile.mkstemp(suffix=".csv", prefix="SampleSheet", dir=cls.samplesheet_dir)
        with open(samplesheet, "w") as ssheeth:
            ssheeth.write(contents)
        return samplesheet

    def setUp(self):
        self.model_handler = mock.MagicMock(spec=BaseModelHandler)
        self.connector = FileSystemConnector(self.samplesheet_dir, model_handler=self.model_handler)

    def test_locate_samplesheet(self):
        self.connector.POSSIBLE_SAMPLESHEET_NAMES = ["samplesheet_alt1.csv", "samplesheet_alt2.csv"]
        with self.assertRaises(SampleSheetNotFoundError):
            self.connector._locate_samplesheet()
        self.connector.POSSIBLE_SAMPLESHEET_NAMES.append(os.path.basename(self.samplesheet))
        self.assertEqual(self.connector._locate_samplesheet(), self.samplesheet)

    def test_samplesheet_to_json_no_data(self):
        samplesheet = self._write_samplesheet(
            contents=self.samplesheet_contents.replace("[Data]", "[Not Data]"))
        with self.assertRaises(SampleSheetFormatNotRecognizedError):
            self.connector._samplesheet_to_json(samplesheet)

    def test_samplesheet_to_json_no_library_name(self):
        samplesheet = self._write_samplesheet(
            contents=self.samplesheet_contents.replace("LIBRARY_NAME", "NOT_LIBRARY_NAME", 1))
        with self.assertRaises(SampleSheetFormatNotRecognizedError):
            self.connector._samplesheet_to_json(samplesheet)

    def test_samplesheet_to_json(self):
        observed_json = self.connector._samplesheet_to_json(self.samplesheet)
        self.assertDictContainsSubset(self.samplesheet_json_sample, observed_json)

    def assertDictContainsSubset(self, subset, dictionary, msg=None):
        for key, value in subset.items():
            self.assertIn(key, dictionary, msg=msg)
            if isinstance(value, dict):
                self.assertDictContainsSubset(value, dictionary[key], msg=msg)
            # TODO: properly recurse through lists
            else:
                self.assertEqual(value, dictionary[key], msg=msg)

    def test_open(self):
        self.connector.open()
        # print(json.dumps(self.connector.json_obj, indent=2))
