""" All HGSC Errors """
from dataclasses import dataclass


@dataclass
class ExemplarWGSInternalIDMissing(Exception):
    """Raised if the wgs_sample_internal_id is invalid."""

    samples: set
    message: str = "Given wgs_sample_external_ids are missing wgs_sample_internal_ids"


@dataclass
class ExemplarMultipleWGSInternalIDs(Exception):
    """Raised if one wgs_sample_external_id has multiple unique wgs_sample_internal_ids"""

    samples: set
    message: str = "Multiple unique wgs_sample_internal_ids were found for the wgs_sample_external_id"


@dataclass
class HGSCWebServiceError(Exception):
    """Raised when sample failed to upload"""

    response: str
    service: str
    method: str
    message: str = "Error using the HGSC web service."
