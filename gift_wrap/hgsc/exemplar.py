from collections import defaultdict
import logging
from typing import DefaultDict, List, Set

from gift_wrap.hgsc.webservice import WebService
from gift_wrap.hgsc.exceptions import (
    ExemplarMultipleWGSInternalIDs,
    ExemplarWGSExternalIDDupes,
    ExemplarWGSInternalIDMissing,
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
        self, wgs_sample_external_ids: List[str]
    ) -> DefaultDict(Set):
        """Given the wgs_sample_external_id, returns a mapping of wgs_sample_internal_ids wgs_sample_internal_id"""
        logger.info("Getting wgs_sample_internal_id...")
        if dupes := {
            x for x in wgs_sample_external_ids if wgs_sample_external_ids.count(x) > 1
        }:
            raise ExemplarWGSExternalIDDupes(dupes)
        url = self.base_url / "sampleservice/sampleInfoByCollaboratorSampleId"
        data = {"sample_ids": wgs_sample_external_ids}
        response = self._post(url, json=data)
        result = defaultdict(set)
        for sample in response["sampleInfo"]:
            wgs_sample_external_id = sample["sample_external_id"]
            result[wgs_sample_external_id] = {sample["sample_internal_id"]}
        if len(result.keys()) != len(wgs_sample_external_ids):
            missing = set(wgs_sample_external_ids) - set(result.keys())
            logger.error(
                "Not all samples returned wgs_sample_internal_ids! %s", missing
            )
            raise ExemplarWGSInternalIDMissing(wgs_sample_external_ids=missing)
        if more_than_one_internal_id := {
            external_id
            for external_id, internal_id in result.items()
            if len(internal_id) > 1
        }:
            raise ExemplarMultipleWGSInternalIDs(more_than_one_internal_id)
        return result

    def get_drc_ready_samples(self):
        """Returns a list of records that represent samples ready to be
        submitted by the DRC. If no samples are ready to be submitted, then
        an empty list is returned."""
        logger.info("Grabbing samples ready to submit to DRC")
        url = self.base_url / "sequencingservice/thresholdCriteriaMet"
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
        url = self.base_url / "sequencingservice/submissionstatus"
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
