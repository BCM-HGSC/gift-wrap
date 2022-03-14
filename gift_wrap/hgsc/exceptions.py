""" All HGSC Errors """
from dataclasses import dataclass


class ExemplarWGSInternalIDInvalid(Exception):
    """Raised if the wgs_sample_internal_id is invalid."""


@dataclass
class HGSCWebServiceError(Exception):
    """Raised when sample failed to upload"""

    response: str
    service: str
    method: str
    message: str = "Error using the HGSC web service."
