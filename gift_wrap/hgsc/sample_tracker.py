"""Wrapper around sample_tracker."""
import logging

from gift_wrap.hgsc.exceptions import HGSCWebServiceError

from .type_defs import APIResponseTypeDef
from .webservice import WebService


logger = logging.getLogger(__name__)


class SampleTracker(WebService):
    """Wrapper for Sample Tracker"""

    def post(
        self,
        wgs_sample_internal_id: str,
        biobank_id: str,
        project: str,
        state_key: str,
        **kwargs
    ) -> APIResponseTypeDef:
        """Post to SampleTracker"""
        logger.info("Uploading sample(%s) to Sample Tracker", wgs_sample_internal_id)
        url = self.base_url / "upsertkudusampletracking"
        record = {
            "biobankid": biobank_id,
            "project": project,
            "samplename": wgs_sample_internal_id,
            "statekey": state_key,
            **kwargs,
        }
        response = self._post(url, record)
        if response["success"] is False:
            raise HGSCWebServiceError(response["content"], __class__.__name__, "POST")
        return response["content"]

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
