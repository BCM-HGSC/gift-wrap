"""Wrapper around sample_tracker."""
import logging

from tenacity import retry, wait_fixed, stop_after_attempt

from .type_defs import APIResponseTypeDef
from .webservice import WebService


logger = logging.getLogger(__name__)


class SampleTracker(WebService):
    """Wrapper for Sample Tracker"""

    @retry(reraise=True, wait=wait_fixed(5), stop=stop_after_attempt(3))
    def post(
        self, sample_name: str, biobank_id: str, project: str, state_key: str, **kwargs
    ) -> APIResponseTypeDef:
        """Post to SampleTracker"""
        logger.info("Uploading sample(%s) to Sample Tracker", sample_name)
        record = {
            "biobankid": biobank_id,
            "project": project,
            "samplename": sample_name,
            "statekey": state_key,
            **kwargs,
        }
        return self._post(record)


# def get_transformed_record(record):
#     """
#     SampleTracker wants the field names to be lowercase with no underscores.
#     Ex: field_named -> fieldname
#     """
#     transformed_record = {}
#     for field, value in record.items():
#         field = "sampleexternalid" if field == "sample_id" else field.replace("_", "")
#         transformed_record[field] = value
#     transformed_record["statekey"] = "bhaou_intake"
#     transformed_record["wellposition"] = "".join(
#         map(str, transformed_record["wellposition"])
#     )
#     transformed_record["project"] = "CLAOU"
#     return transformed_record


# def get_generic_transformed_record(record: Dict, state: str) -> Dict:
#     """
#     Returns generic transformed record.
#     """
#     return {
#         "biobankid": record["biobank_id"],
#         "project": "CLAOU",
#         "samplename": record["lims_id"],
#         "statekey": state,
#     }


# def get_fingerprint_sample(biobank_id):
#     """Returns a sample ready for fingerprint submission"""
#     return {
#         "biobankid": biobank_id,
#         "project": "CLAOU",
#         "samplename": biobank_id,
#         "statekey": "CONCORDANCE_FILE_GRAB",
#     }
