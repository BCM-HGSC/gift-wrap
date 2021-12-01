""" Houses HGSC Web Service Type Definitions to help with typing """
from typing import TypedDict


class APIResponseTypeDef(TypedDict):
    """Type definition for HGSC API Response"""

    success: bool
    content: str
