""" Generic class for an HGSC web service to inherit """
import logging
import json
from typing import Dict, Any

from requests.exceptions import HTTPError

import yarl

from gift_wrap.utils.http import http
from gift_wrap.hgsc.exceptions import HGSCWebServiceError
from gift_wrap.hgsc.type_defs import APIResponseTypeDef


logger = logging.getLogger(__name__)


class WebService:
    """Generic wrapper for HGSC Web Services"""

    def __init__(self, token: str, base_url: str, verify_ssl: bool = True):
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.base_url = yarl.URL(base_url)
        self.verify_ssl = verify_ssl

    def _get(self, url: str, data: str):
        """Get to HGSC endpoint"""
        logger.debug("GET to %s", url)
        data = json.dumps(data, default=str)
        try:
            response = http.get(url, data=data, headers=self.headers)
        except HTTPError as err:
            raise_hgscwebserviceerror(self.__class__.__name__, err, "GET")
        return response.json()

    def _post(self, url: str, data: Dict[str, Any]) -> APIResponseTypeDef:
        """Post to HGSC endpoint"""
        data = json.dumps(data, default=str)
        try:
            response = http.post(url, data=data, headers=self.headers)
        except HTTPError as err:
            raise_hgscwebserviceerror(self.__class__.__name__, err, "POST")
        return response.json()

    def __repr__(self):
        return f"{self.__class__.__name__}(url: {self.base_url})"


def raise_hgscwebserviceerror(class_name: str, err, method: str) -> None:
    """Raises an HGSCWebServiceError when a HTTPError is returned"""
    error = err.response.text or err
    logger.error(error)
    raise HGSCWebServiceError(
        response=error, method=method, service=class_name
    ) from err
