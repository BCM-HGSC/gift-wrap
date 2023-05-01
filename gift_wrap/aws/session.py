# pylint: disable=too-many-arguments

from typing import Optional

import boto3
from botocore.session import Session
from botocore.config import Config


class AWSSessionBase:
    """Base AWS Session"""

    def __init__(
        self,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        session_token: Optional[str] = None,
        region_name: Optional[str] = None,
        botocore_session: Optional[Session] = None,
        profile_name: Optional[str] = None,
        config: str = "standard",
    ) -> None:
        self.config = Config(retries={"mode": config})
        self.session = boto3.Session(
            access_key_id,
            secret_access_key,
            session_token,
            region_name,
            botocore_session,
            profile_name,
        )
