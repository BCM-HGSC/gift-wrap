""" All HGSC Errors """
from dataclasses import dataclass


@dataclass
class HGSCWebServiceError(Exception):
    """Raised when sample failed to upload"""

    response: str
    service: str
    method: str
    message: str = "Error using the HGSC web service."
