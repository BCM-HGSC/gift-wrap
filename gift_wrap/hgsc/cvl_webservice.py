""" HGSC's CVL API """
# pylint: disable=too-few-public-methods
# Disabling since intake only needs to ever POST

import logging
from datetime import datetime, timezone
from typing import Dict, List

from tenacity import retry, wait_fixed, stop_after_attempt

from gift_wrap.hgsc.type_defs import APIResponseTypeDef
from gift_wrap.hgsc.webservice import WebService


logger = logging.getLogger(__name__)


class CVLWebservice(WebService):
    """CVL Webservice Wrapper"""

    @retry(reraise=True, wait=wait_fixed(5), stop=stop_after_attempt(3))
    def post(
        self, manifest_type: str, s3_path: str, data: List[Dict[str, str]]
    ) -> APIResponseTypeDef:
        """Post to the CVL webservice"""
        logger.info("Submitting to CVL Webservice...")
        record = {
            "manifest_name": manifest_type,
            "s3_location": s3_path,
            "timestamp": str(datetime.now(timezone.utc).isoformat()),
            "data": data,
        }
        self._post(record)
