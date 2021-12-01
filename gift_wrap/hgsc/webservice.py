""" Generic class for an HGSC web service to inherit """
import logging
import json
from typing import Dict, Any

import requests

from gift_wrap.hgsc.exceptions import HGSCWebServiceError
from gift_wrap.hgsc.type_defs import APIResponseTypeDef


logger = logging.getLogger(__name__)


class WebService:
    """Generic wrapper for HGSC Web Services"""

    def __init__(self, token: str, url: str, verify_ssl: bool = True):
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.url = url
        self.verify_ssl = verify_ssl

    def _post(self, record: Dict[str, Any]) -> APIResponseTypeDef:
        """Post to HGSC endpoint"""
        data = json.dumps(record, default=str)
        try:
            response = requests.post(self.url, data=data, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            error = err.response.text or err
            logger.error(error)
            raise HGSCWebServiceError(
                response=error, service=self.__class__.__name__
            ) from err
        # In the off chance an error occured but returns 200
        response = response.json()
        if response["success"] is False:
            raise HGSCWebServiceError(
                response=response["content"], service=self.__class__.__name__
            )
        return response

    def __repr__(self):
        return f"{self.__class__.__name__}(url: {self.url})"
