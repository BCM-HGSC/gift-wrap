""" All HGSC Errors """
from dataclasses import dataclass


@dataclass
class HGSCWebServiceError(Exception):
    """Raised when sample failed to upload"""

    response: str
    service: str
    message: str = "Unable to post to the HGSC web service."
