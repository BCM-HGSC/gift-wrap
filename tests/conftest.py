from datetime import datetime

import pytest

APP_NAME = "gift-wrap"
TIMESTAMP = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def pytest_addoption(parser):
    parser.addoption("--gcp_bucket", action="store", default="gcp bucket name")
    parser.addoption("--s3_bucket", action="store", default="s3 bucket name")


@pytest.fixture(name="prefix")
def fixture_prefix():
    return f"{APP_NAME}-{TIMESTAMP}"
