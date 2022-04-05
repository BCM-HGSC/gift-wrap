from collections import defaultdict
import logging
from typing import DefaultDict, Set

from gift_wrap.hgsc.webservice import WebService
from gift_wrap.hgsc.exceptions import (
    ExemplarWGSInternalIDMissing,
    ExemplarMultipleWGSInternalIDs,
    HGSCWebServiceError,
)

logger = logging.getLogger(__name__)


INVALID_INTERNAL_ID_MSG = (
    "wgs_sample_external_id({wgs_sample_external_id}) is "
    "associated with none or multiple internal ids: "
    "{wgs_sample_internal_id}"
)


class ExemplarAPI(WebService):
    """Wrapper around Exemplar LIMS API"""

    def __init__(self, token: str, base_url: str, verify_ssl: bool = True):
        super().__init__(token, base_url, verify_ssl)
        self.headers = {"Auth-Code": token}

    def get_wgs_sample_internal_ids(
        self, wgs_sample_external_ids: Set
    ) -> DefaultDict(Set):
        """Given the wgs_sample_external_id, returns a mapping of wgs_sample_internal_ids wgs_sample_internal_id"""
        logger.info("Getting wgs_sample_internal_id...")
        url = self.base_url / "qcCompletionByCollaboratorSampleId"
        response = self._get(url, params={"sampleId": wgs_sample_external_ids})
        result = defaultdict(set)
        for sample in response["qcCompletionBySampleIdInfo"]:
            wgs_sample_external_id = sample["collaborator_sample_id"]
            qc_info_list = sample["qcCompletionInfo"]
            for sample_qc in qc_info_list:
                result[wgs_sample_external_id].add(sample_qc["lims_id"])
        if len(result.keys()) != len(wgs_sample_external_ids):
            missing = wgs_sample_external_ids - set(result.keys())
            logger.error(
                "Not all samples returned wgs_sample_internal_ids! %s", missing
            )
            raise ExemplarWGSInternalIDMissing(samples=missing)
        if multiple_ids := {
            external_id
            for external_id, internal_ids in result.items()
            if len(internal_ids) > 1
        }:
            logger.error(
                "Multiple unique wgs_sample_internal_ids were returned. %s",
                multiple_ids,
            )
            raise ExemplarMultipleWGSInternalIDs(samples=multiple_ids)
        return result

    def get_drc_ready_samples(self):
        """Returns a list of records that represent samples ready to be
        submitted by the DRC. If no samples are ready to be submitted, then
        an empty list is returned."""
        logger.info("Grabbing samples ready to submit to DRC")
        url = self.base_url / "thresholdCriteriaMet"
        return self._get(
            url,
            params={"eligibleFor": "DRC"},
        )["thresholdCriteriaInfo"]

    def push_sample_success(self, lane_barcode_or_merge_name: str, submission_date):
        """
        Post sucess status for sample submission status
        If an issue is encountered, UnableToPushSampleSuccess is raised.
        """
        logger.info("Pushing success to DRC: %s", lane_barcode_or_merge_name)
        url = self.base_url / "submissionstatus"
        payload = {
            "eventTimestamp": submission_date,
            "submissionValue": "True",
            "laneBarcodeOrMergeName": lane_barcode_or_merge_name,
            "submissionType": "DRC",
        }
        response = self._post(url, json=payload)
        if not response["success"]:
            raise HGSCWebServiceError(response["message"], __class__.__name__, "POST")
        return response
