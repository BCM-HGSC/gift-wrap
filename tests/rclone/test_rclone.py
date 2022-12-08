import os
from pathlib import Path

from gift_wrap import rclone
from gift_wrap.utils.utils import load_json_file


def test_copy_to_no_extra_args(tmp_path: Path):
    """Test that rclone correctly runs.
    NOTE: This needs rclone installed in the environment"""
    txt_file = tmp_path / "file.txt"
    txt_file.write_text("Test")
    rclone_config = tmp_path / "rclone_config.ini"
    rclone_config.write_text("")
    dest_folder = tmp_path / "test_location"
    dest_folder.mkdir(exist_ok=True)
    dest = dest_folder / "another_file.txt"
    result = rclone.copy_to(str(txt_file), str(dest), str(rclone_config))
    assert result.returncode == 0
    assert dest.exists()


def test_convert_cloud_path():
    """Test that a cloud path is correctly converted to the
    expected rclone format"""
    cloud_path = "s3://bucket_name/prefix/fake.csv"
    result = rclone.convert_cloud_path(cloud_path)
    assert result == "s3:bucket_name/prefix/fake.csv"


def test_create_rclone_config(tmp_path: Path):
    """Verify that an rclone_config is correctly generated"""
    credentials_file = os.environ["GCP_CREDENTIALS_PATH"]
    project_id = load_json_file(credentials_file)["project_id"]
    result_path = rclone.create_rclone_config(credentials_file, tmp_path)
    with open(result_path, "r", encoding="utf-8") as fout:
        result = fout.read()
        assert (
            result
            == f"""
[s3]
type = s3
provider = AWS
env_auth = true
no_check_bucket = true
region = us-east-1

[gs]
type = google cloud storage
project_number = {project_id}
service_account_file = {credentials_file}
"""
        )


def test_get_gcp_project_id():
    """Assert that the method returns the expected GCP service account
    project id"""
    credentials_file = os.environ["GCP_CREDENTIALS_PATH"]
    result = rclone.rclone.get_gcp_project_id(credentials_file)
    assert result == load_json_file(credentials_file)["project_id"]
