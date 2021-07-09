import logging
import json
import os
from typing import Dict

from .exceptions import SampleTrackerMissingVariableError, SampleTrackerFailedUpload
from ..utils.requests import http

logger = logging.getLogger(__name__)

TOKEN   = os.environ.get("SAMPLE_TRACKER_TOKEN")
URL     = os.environ.get("SAMPLE_TRACKER_URL")


if not TOKEN or not URL:
    raise SampleTrackerMissingVariableError


class SampleTracker:
    def __init__(self) -> None:
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        }

    def post(self, record: Dict) -> Dict:
        """
        Submits a record to Sample Tracker.
        """
        logger.info(f"Uploading sample to Sample Tracker")
        json_record = json.dumps(record, default=str)
        try:
            response = http.post(URL, data=json_record, headers=self.headers)
            response.raise_for_status()
        except Exception as e:
            error = e.response.text or e
            msg = f"Unable to upload sample status to sample_tracker. {error}"
            logger.error(msg)
            raise SampleTrackerFailedUpload(msg) from e
        # In the off chance an error occured but returns 200
        response = response.json()
        if response["success"] == False:
            raise SampleTrackerFailedUpload(response["content"])
        return response["content"]
