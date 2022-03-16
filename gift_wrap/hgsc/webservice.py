""" Generic class for an HGSC web service to inherit """
from distutils.util import strtobool
import logging
import json
from typing import Optional, Union

from requests.exceptions import HTTPError

import yarl

from gift_wrap.utils.http import http
from gift_wrap.hgsc.exceptions import HGSCWebServiceError
from gift_wrap.hgsc.type_defs import APIResponseTypeDef


logger = logging.getLogger(__name__)


class WebService:
    """Generic wrapper for HGSC Web Services"""

    def __init__(
        self, token: str, base_url: str, verify_ssl: Optional[Union[str, bool]] = True
    ):
        self.headers = {
            "Accept": "application/json",
            "Accept-Enconding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.base_url = yarl.URL(base_url)
        self.verify_ssl = verify_ssl
        if isinstance(self.verify_ssl, str) and self.verify_ssl.lower() in [
            "true",
            "false",
        ]:
            self.verify_ssl = bool(strtobool(self.verify_ssl))

    def _get(self, url: str, **kwargs):
        """Get to HGSC endpoint"""
        logger.debug("GET to %s", url)
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"], default=str)
        try:
            response = http.get(
                url, headers=self.headers, verify=self.verify_ssl, **kwargs
            )
        except HTTPError as err:
            raise_hgscwebserviceerror(self.__class__.__name__, err, "GET")
        return response.json()

    def _post(self, url: str, **kwargs) -> APIResponseTypeDef:
        """Post to HGSC endpoint"""
        try:
            response = http.post(
                url, headers=self.headers, verify=self.verify_ssl, **kwargs
            )
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
