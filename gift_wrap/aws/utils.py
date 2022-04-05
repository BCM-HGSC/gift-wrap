import os
from typing import Dict


def do_env_variables_exists() -> bool:
    """Method that returns a bool whether all the required varaibles exists or
    not"""
    return bool(
        os.environ.get("AWS_ACCESS_KEY_ID")
        or os.environ.get("AWS_DEFAULT_REGION")
        or os.environ.get("AWS_SECRET_ACCESS_KEY")
        or os.environ.get("AWS_SESSION_TOKEN")
    )


def get_session_kwargs() -> Dict[str, str]:
    """Gets the appropriate session kwargs"""
    if do_env_variables_exists():
        return {
            "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
            "aws_session_token": os.environ.get("AWS_SESSION_TOKEN"),
            "region_name": os.environ.get("AWS_DEFAULT_REGION"),
        }
    return {"profile_name": os.environ.get("AWS_PROFILE") or "default"}
