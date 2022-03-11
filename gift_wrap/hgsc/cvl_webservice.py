""" HGSC's CVL API """
# pylint: disable=too-few-public-methods
# Disabling since intake only needs to ever POST

import logging
from datetime import datetime, timezone
from typing import Dict, List

from gift_wrap.hgsc.type_defs import APIResponseTypeDef
from gift_wrap.hgsc.webservice import WebService


logger = logging.getLogger(__name__)


class CVLWebservice(WebService):
    """CVL Webservice Wrapper"""

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
