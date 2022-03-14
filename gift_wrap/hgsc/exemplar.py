import logging

from gift_wrap.hgsc.webservice import WebService
from gift_wrap.hgsc.exceptions import ExemplarWGSInternalIDInvalid, HGSCWebServiceError

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

    def get_wgs_sample_internal_id(self, wgs_sample_external_id: str) -> str:
        """Given the wgs_sample_external_id, returns the wgs_sample_internal_id"""
        logger.info("Getting wgs_sample_internal_id...")
        url = self.base_url / "thresholdCriteriaMet"
        response = self._get(
            url, params={"wgs_sample_external_id": wgs_sample_external_id}
        )
        wgs_sample_internal_id = response["lims_id"]
        if not wgs_sample_internal_id or len(wgs_sample_internal_id) > 1:
            raise ExemplarWGSInternalIDInvalid(
                INVALID_INTERNAL_ID_MSG.format(
                    wgs_sample_external_id=wgs_sample_external_id,
                    wgs_sample_internal_id=wgs_sample_internal_id,
                )
            )

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
