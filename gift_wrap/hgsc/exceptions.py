""" All HGSC Errors """
from dataclasses import dataclass
from typing import Set


@dataclass
class GETWGSSampleInternalIDError(Exception):
    """Generic exception for when getting a wgs_sample_internal_id"""


@dataclass
class CVLAPIWGSSampleInternalIDError(GETWGSSampleInternalIDError):
    """Raised any issue for cvl api getting wgs_sample_internal_id"""

    wgs_sample_external_id: str


@dataclass
class CVLAPIIssuesGettingInternalID(CVLAPIWGSSampleInternalIDError):
    """Raised if there is an issue getting an wgs_sample_internal id"""

    message: str = "No wgs_sample_internal_id was returned"


@dataclass
class CVLAPIMultipleWGSInternalIDs(CVLAPIWGSSampleInternalIDError):
    """Raised if there is an issue getting an wgs_sample_internal id"""

    message: str = "Multiple unique wgs_sample_internal_ids were found for the wgs_sample_external_id"


@dataclass
class ExemplarWGSSampleInternalIDError(GETWGSSampleInternalIDError):
    """Raised any issue for cvl api getting wgs_sample_internal_id"""

    wgs_sample_external_ids: Set


@dataclass
class ExemplarWGSInternalIDMissing(ExemplarWGSSampleInternalIDError):
    """Given wgs_sample_external_ids are missing wgs_sample_internal_ids."""

    message: str = "Given wgs_sample_external_ids are missing wgs_sample_internal_ids"


@dataclass
class ExemplarMultipleWGSInternalIDs(ExemplarWGSSampleInternalIDError):
    """Raised if one wgs_sample_external_id has multiple unique wgs_sample_internal_ids"""

    message: str = "Multiple unique wgs_sample_internal_ids were found for the wgs_sample_external_id"


@dataclass
class HGSCWebServiceError(Exception):
    """Raised when sample failed to upload"""

    response: str
    service: str
    method: str
    message: str = "Error using the HGSC web service."
