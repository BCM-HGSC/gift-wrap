import contextlib
import os
from pathlib import Path

import pytest

from gift_wrap.aws.s3 import S3Resource


INPUT_FILE_NAME = "test_file.txt"


@pytest.fixture(name="bucket_name")
def fixture_bucket_name(pytestconfig: pytest.Config):
    """Returns the S3 bucket name. Prefers the given one by command line if
    looks in env"""
    if s3_bucket_name := pytestconfig.getoption(
        "s3_bucket", default=None
    ) or os.environ.get("S3_BUCKET_NAME"):
        return s3_bucket_name
    raise ValueError("Missing S3 bucket name. Pass it by command line or have in .env")


@pytest.fixture(name="s3_client")
def fixture_s3_client(bucket_name: str, prefix: str):
    """Fixture that returns a S3Resource and cleans up afterwards."""
    client = S3Resource(bucket_name)
    yield client
    objects = client.list_files(prefix=prefix)
    with contextlib.suppress(Exception):
        for obj in objects:
            obj.delete()


@pytest.fixture(name="populated_s3_client")
def fixture_populated_s3_client(s3_client: S3Resource, prefix: str, tmp_path: Path):
    """
    A fixture that will populate the s3 client with one file.
    """
    input_file = tmp_path / INPUT_FILE_NAME
    input_file.write_text("Tests file")
    destination = f"{prefix}/{INPUT_FILE_NAME}"
    s3_client.upload_file(str(input_file), destination)
    yield s3_client


def test_s3resource_delete_file(populated_s3_client: S3Resource, prefix: str):
    """Test that a file is successfully uploaded"""
    client = populated_s3_client
    remote_file = f"{prefix}/{INPUT_FILE_NAME}"
    client.delete_file(remote_file)
    assert not list(client.list_files(prefix))


def test_s3resource_download_file(
    populated_s3_client: S3Resource, prefix: str, tmp_path: Path
):
    """Test that a file is successfully downloaded"""
    remote_file = f"{prefix}/{INPUT_FILE_NAME}"
    local_path = tmp_path / INPUT_FILE_NAME
    populated_s3_client.download_file(remote_file, str(local_path))
    assert local_path.exists()


def test_s3resource_list_files(populated_s3_client: S3Resource, prefix: str):
    """Test that the client successfully list the objects given a prefix"""
    results = list(populated_s3_client.list_files(prefix))
    assert len(results) == 1


def test_s3resource_upload_file(s3_client: S3Resource, prefix: str, tmp_path: Path):
    """Test that a file is successfully uploaded"""
    input_file = tmp_path / "gift-wrap-input.txt"
    input_file.write_text("Tests file")
    upload_dir = f"{prefix}/upload-test"
    destination = f"{upload_dir}/gift_wrap-input.txt"
    s3_client.upload_file(str(input_file), destination)
    results = list(s3_client.list_files(upload_dir))
    assert len(results) == 1
    assert results[0].key == destination


def test_s3resource_upload_dir_to_bucket(
    s3_client: S3Resource, prefix: str, tmp_path: Path
):  # sourcery skip: avoid-builtin-shadow
    """
    Test that a directory is successfully uploaded to s3.
    """
    tmp_dir = tmp_path / "upload-test"
    tmp_dir.mkdir()
    file_one = tmp_dir / "hello.txt"
    file_one.write_text("content")
    file_two = tmp_dir / "bye.txt"
    file_two.write_text("content")
    s3_client.upload_dir_to_bucket(prefix, tmp_dir)
    objects = list(s3_client.list_files(f"{prefix}/upload-test"))
    assert len(objects) == 2
