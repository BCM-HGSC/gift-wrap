"""Test for gcp.py"""
import os
from pathlib import Path

import pytest

from gift_wrap.gcp.cloud_storage import StorageClient


INPUT_FILE_NAME = "test_file.txt"


@pytest.fixture(name="bucket_name")
def fixture_bucket_name(pytestconfig):
    """Returns the GCP bucket name. Prefers the given one by command line if
    looks in env"""
    bucket_name = pytestconfig.getoption("gcp_bucket", default=None) or os.environ.get(
        "GCP_BUCKET_NAME"
    )
    if not bucket_name:
        raise ValueError(
            "Missing GCP bucket name. Pass it by command line or have in .env"
        )
    return bucket_name


@pytest.fixture(name="gcp_client")
def fixture_gcp_client(bucket_name: str, prefix: str):
    """Fixture that returns a StorageClient and cleans up afterwards."""
    credentials_file = os.environ["GCP_CREDENTIALS_PATH"]
    client = StorageClient(bucket_name, credentials_file=credentials_file)
    yield client
    blobs = client.list_files(prefix=prefix)
    try:
        for blob in blobs:
            blob.delete()
    except Exception:
        pass


@pytest.fixture(name="populated_gcp_client")
def fixture_populated_gcp_client(gcp_client: StorageClient, prefix: str, tmp_path: Path):
    """
    A fixture that will populate the gcp client with one file.
    """
    input_file = tmp_path / INPUT_FILE_NAME
    input_file.write_text("Tests file")
    destination = f"{prefix}/{INPUT_FILE_NAME}"
    gcp_client.upload_file(input_file, destination)
    yield gcp_client


def test_storageclient_delete_file(populated_gcp_client: StorageClient, prefix: str):
    """Test that a file is successfully uploaded"""
    client = populated_gcp_client
    remote_file = f"{prefix}/{INPUT_FILE_NAME}"
    client.delete_file(remote_file)
    assert not list(client.list_files(prefix))


def test_storageclient_download_file(
    populated_gcp_client: StorageClient, prefix: str, tmp_path: Path
):
    """Test that a file is successfully downloaded"""
    remote_file = f"{prefix}/{INPUT_FILE_NAME}"
    local_path = tmp_path / INPUT_FILE_NAME
    populated_gcp_client.download_file(remote_file, local_path)
    assert local_path.exists()


def test_storageclient_list_files(populated_gcp_client: StorageClient, prefix: str):
    """Test that the client successfully list the objects given a prefix"""
    results = list(populated_gcp_client.list_files(prefix))
    assert len(results) == 1


def test_storageclient_upload_file(gcp_client: StorageClient, prefix: str, tmp_path: Path):
    """Test that a file is successfully uploaded"""
    input_file = tmp_path / "gift-wrap-input.txt"
    input_file.write_text("Tests file")
    upload_dir = f'{prefix}/upload-test'
    destination = f'{upload_dir}/gift_wrap-input.txt'
    gcp_client.upload_file(input_file, destination)
    results = list(gcp_client.list_files(upload_dir))
    assert len(results) == 1
    assert results[0].name == destination
