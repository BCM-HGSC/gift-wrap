""" HGSC's CVL API """
# pylint: disable=too-few-public-methods
# Disabling since intake only needs to ever POST

import logging
from datetime import datetime, timezone

from gift_wrap.hgsc.exceptions import (
    CVLAPIIssuesGettingInternalID,
    CVLAPIMultipleWGSInternalIDs,
    HGSCWebServiceError,
)
from gift_wrap.hgsc.webservice import WebService


logger = logging.getLogger(__name__)

BATCH_SIZE = 100


class CVLAPI(WebService):
    """CVL Webservice Wrapper"""

    def get_wgs_sample_internal_id(self, wgs_sample_external_id: str) -> str:
        """Given the wgs_sample_external_id, grabs the wgs_sample_internal_id"""
        logger.info("%s: Getting wgs_sample_internal_id", wgs_sample_external_id)
        url = self.base_url / "getDynamodbAouData"
        data = {
            "projection_expression": "wgs_sample_internal_id",
            "filter_expression": {"wgs_sample_external_id": wgs_sample_external_id},
        }
        response = self._get(url, data=data)
        if response["success"] is False:
            raise HGSCWebServiceError(
                response["content"], service=__class__.__name__, method="GET"
            )
        if not response["content"]:
            raise CVLAPIIssuesGettingInternalID(
                wgs_sample_external_id=wgs_sample_external_id,
                message=f"No wgs_sample_internal_id was returned for {wgs_sample_external_id}",
            )
        if len(response["content"]) > 1:
            raise CVLAPIMultipleWGSInternalIDs(
                wgs_sample_external_id=wgs_sample_external_id,
                message=f"Multiple wgs_sample_internal_ids were returned for {wgs_sample_external_id}",
            )
        return response["content"][0]["wgs_sample_internal_id"]

    def post(self, manifest_group: str, s3_path: str, **kwargs) -> int:
        """Post to the CVL webservice"""
        logger.info("Submitting to CVL Webservice...")
        url = self.base_url / "putBatchAouData2Dynamodb"
        data = {
            "manifest_name": manifest_group.lower(),
            "file_s3_location": s3_path,
        }
        if "manifest_records" in kwargs:
            records = kwargs["manifest_records"]
            records_uploaded = 0
            for batch_number in range(0, len(records), BATCH_SIZE):
                records_batch = records[batch_number : batch_number + BATCH_SIZE]
                data |= {
                    "timestamp": str(datetime.now(timezone.utc).isoformat()),
                    "data": records_batch,
                }
                logger.info("Submitting batch %s", batch_number)
                self._post(url, json=data)
                records_uploaded += len(records_batch)
            return records_uploaded
        data = {
            "timestamp": str(datetime.now(timezone.utc).isoformat()),
            **kwargs,
        }
        self._post(url, json=data)
        return 1
