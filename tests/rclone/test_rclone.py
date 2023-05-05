import contextlib
from pathlib import Path

import pytest

from gift_wrap import rclone
from gift_wrap.gcp.cloud_storage import StorageClient


@pytest.fixture(name="gcp_client")
def fixture_gcp_client(prefix: str, pytestconfig):
    """Fixture that returns a StorageClient and cleans up afterwards."""
    bucket_name = pytestconfig.getoption("gcp_bucket")
    client = StorageClient(bucket_name)
    yield client
    blobs = client.list_files(prefix=prefix)
    with contextlib.suppress(Exception):
        for blob in blobs:
            blob.delete()


@pytest.fixture(name="rclone_wrapper")
def fixture_rclone_wrapper(tmp_path: Path):
    """Creates rclone class using the basic config path"""
    config_path = rclone.create_generic_config(tmp_path)
    yield rclone.RClone(config_path)


def test_copy_to(rclone_wrapper: rclone.RClone, tmp_path: Path):
    """Test that rclone correctly runs.
    NOTE: This needs rclone installed in the environment"""
    txt_file = tmp_path / "file.txt"
    txt_file.write_text("Test")
    dest_folder = tmp_path / "test_location"
    dest_folder.mkdir(exist_ok=True)
    dest = dest_folder / "another_file.txt"
    result = rclone_wrapper.copy_to(str(txt_file), str(dest))
    assert result.returncode == 0
    assert dest.exists()


def test_list_contents_nonempty(
    prefix: str,
    gcp_client: StorageClient,
    rclone_wrapper: rclone.RClone,
    tmp_path: Path,
):
    """Test that rclone correctly returns a dictionary of list files and list of
    directories."""
    # Further Set Up
    file_one_name = "file001-rclone-test_list_contents.txt"
    file = tmp_path / file_one_name
    file.write_text("Tests file")
    gcp_client.upload_file(str(file), f"{prefix}/{file_one_name}")
    # Now create subdir + file
    file_002 = tmp_path / "file002-rclone-test_list_contents.txt"
    file_002.write_text("Tests file")
    sub_dir = "test_list_contents"
    gcp_client.upload_file(
        str(file_002), f"{prefix}/{sub_dir}/file002-rclone-test_list_contents.txt"
    )
    dest = f"gs://{gcp_client.bucket.name}/{prefix}"
    result = rclone_wrapper.list_contents(dest)
    assert result["files"] == [file_one_name]
    assert result["directories"] == [f"{sub_dir}/"]


def test_list_contents_empty(
    prefix: str,
    gcp_client: StorageClient,
    rclone_wrapper: rclone.RClone,
    tmp_path: Path,
):
    """Test that rclone correctly returns a dictionary of list files and list of
    directories."""
    sub_dir = "test_list_contents_madeup"
    dest = f"gs://{gcp_client.bucket.name}/{prefix}/{sub_dir}"
    result = rclone_wrapper.list_contents(dest)
    assert result["files"] == []
    assert result["directories"] == []


def test_create_rclone_config(tmp_path: Path):
    """Verify that an rclone_config is correctly generated"""
    result_path = rclone.create_generic_config(tmp_path)
    with open(result_path, "r", encoding="utf-8") as fout:
        result = fout.read()
        assert (
            result
            == """
[s3]
type = s3
provider = AWS
env_auth = true
no_check_bucket = true

[gs]
type = google cloud storage
env_auth = true

[local]

"""
        )
