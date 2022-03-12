""" HGSC's CVL API """
# pylint: disable=too-few-public-methods
# Disabling since intake only needs to ever POST

import logging
from datetime import datetime, timezone
from typing import Dict, List
from gift_wrap.hgsc.exceptions import HGSCWebServiceError

from gift_wrap.hgsc.type_defs import APIResponseTypeDef
from gift_wrap.hgsc.webservice import WebService


logger = logging.getLogger(__name__)


class CVLAPI(WebService):
    """CVL Webservice Wrapper"""

    def get_wgs_sample_internal_id(self, wgs_sample_external_id: str) -> str:
        """Given the wgs_sample_external_id, grabs the wgs_sample_internal_id"""
        logger.info("%s: Grabing wgs_sample_internal_id", wgs_sample_external_id)
        url = self.base_url / "getDynamodbAouData"
        data = {
            "projection_expression": "wgs_sample_internal_id",
            "filter_expression": {"wgs_sample_external_id": wgs_sample_external_id},
        }
        response = self._get(url, data)
        if response["success"] is False:
            raise HGSCWebServiceError(
                response["content"], service=__class__.__name__, method="GET"
            )
        if not response["content"]:
            raise HGSCWebServiceError(
                response["content"],
                service=__class__.__name__,
                method="GET",
                message=f"No wgs_sample_internal_id was returned for {wgs_sample_external_id}",
            )
        if len(response["content"]) > 1:
            raise HGSCWebServiceError(
                response["content"],
                service=__class__.__name__,
                method="GET",
                message=f"Multiple wgs_sample_internal_ids were returned for {wgs_sample_external_id}",
            )
        return response["content"]

    def post_manifest(
        self, manifest_type: str, s3_path: str, records: List[Dict[str, str]]
    ) -> APIResponseTypeDef:
        """Post to the CVL webservice"""
        logger.info("Submitting to CVL Webservice...")
        url = self.base_url / "putBatchAouData2Dynamodb"
        data = {
            "manifest_name": manifest_type.lower(),
            "s3_location": s3_path,
            "timestamp": str(datetime.now(timezone.utc).isoformat()),
            "data": records,
        }
        return self._post(url, data)
