"""Wrapper around sample_tracker."""
import logging
import json

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
        response = self._post(url, data=json.dumps(record, default=str))
        if response["success"] is False:
            raise HGSCWebServiceError(response["content"], __class__.__name__, "POST")
        return response["content"]
