"""Wrapper around sample_tracker."""

import logging
import json

from .webservice import WebService


logger = logging.getLogger(__name__)

TOP_LEVEL_FIELDS = {"biobank_id", "sample_external_id", "test_code"}


class SampleTracker(WebService):
    """Wrapper for Sample Tracker"""

    def post(self, sample_name: str, project: str, state_key: str, **kwargs):
        """Post to SampleTracker"""
        logger.info("Uploading sample(%s) to Sample Tracker", sample_name)
        extras = {
            field.replace("_", ""): kwargs.pop(field)
            for field in TOP_LEVEL_FIELDS
            if field in kwargs
        }
        record = {
            "project": project,
            "samplename": sample_name,
            "statekey": state_key,
            **extras,
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
