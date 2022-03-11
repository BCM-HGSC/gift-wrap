import os
from datetime import datetime

import pytest

APP_NAME = "gift-wrap"
TIMESTAMP = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def pytest_addoption(parser):
    """Add customizable bucket names for testing through cli"""
    parser.addoption("--gcp_bucket", action="store", default=os.environ.get(
        "GCP_BUCKET_NAME"
    ))
    parser.addoption("--s3_bucket", action="store", default=os.environ.get(
        "S3_BUCKET_NAME"
    ))


@pytest.fixture(name="prefix")
def fixture_prefix():
    """Fixture for a default prefix to use throughout testing. Ex: for folder
    names."""
    return f"{APP_NAME}-{TIMESTAMP}"
