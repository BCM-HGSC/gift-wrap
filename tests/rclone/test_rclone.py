import os
from pathlib import Path

import pytest

from gift_wrap import rclone
from gift_wrap.utils.utils import load_json_file


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
