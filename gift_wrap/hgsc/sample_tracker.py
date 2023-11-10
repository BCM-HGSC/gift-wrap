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
        self, sample_name: str, project: str, state_key: str, **kwargs
    ) -> APIResponseTypeDef:
        """Post to SampleTracker"""
        logger.info("Uploading sample(%s) to Sample Tracker", sample_name)
        record = {
            "project": project,
            "samplename": sample_name,
            "statekey": state_key,
            **kwargs,
        }
        response = self._post(self.url, data=json.dumps(record, default=str))
        if response["success"] is False:
            raise HGSCWebServiceError(response["content"], __class__.__name__, "POST")
        return response["content"]
