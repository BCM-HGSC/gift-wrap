"""Wrapper around sample_tracker."""
import logging
import json

from .webservice import WebService


logger = logging.getLogger(__name__)


class SampleTracker(WebService):
    """Wrapper for Sample Tracker"""

    def post(self, sample_name: str, project: str, state_key: str, **kwargs):
        """Post to SampleTracker"""
        logger.info("Uploading sample(%s) to Sample Tracker", sample_name)
        record = {
            "project": project,
            "samplename": sample_name,
            "statekey": state_key,
            **kwargs,
        }
        response = self._post(self.base_url, data=json.dumps(record, default=str))[
            "SendMessageResponse"
        ]
        logger.info(
            "Sample Name: %s, Message Request ID: %s, Message ID: %s",
            sample_name,
            response["ResponseMetadata"]["RequestId"],
            response["SendMessageResult"]["MessageId"],
        )
        return response
