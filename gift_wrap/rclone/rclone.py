from pathlib import Path
from subprocess import CompletedProcess

from gift_wrap.utils.utils import load_json_file, subprocess_cmd


def copy_to(source: str, dest: str, rclone_config: str) -> CompletedProcess:
    """Uses rclone to copy file from GCP to s3"""
    command = [
        "rclone",
        "--config",
        rclone_config,
        "copyto",
        source,
        dest,
        "--checksum",
        "--error-on-no-transfer",
        "-vv",
    ]
    return subprocess_cmd(command)


def convert_cloud_path(path: str) -> str:
    """Converts the cloud path to the format that rclone prefers"""
    bucket_name = path.split("/")[2]
    cloud_service = path.split("/")[0]
    key = "/".join(path.split("/")[3:])
    return f"{cloud_service}{bucket_name}/{key}"


def create_rclone_config(
    credentials_path: str, working_dir: Path, region: str = "us-east-1"
) -> str:
    """Creates the config for rclone"""
    gcp_project_id = get_gcp_project_id(credentials_path)
    config_path = working_dir / "intake-gvcf-tmp-rclone.conf"
    with open(config_path, "w", encoding="utf-8") as fout:
        fout.write(
            RCLONE_CONFIG_TEMPLATE.format(
                GCP_PROJECT_ID=gcp_project_id,
                GCP_CRED_PATH=credentials_path,
                REGION=region,
            )
        )
    return str(config_path)


def get_gcp_project_id(gcp_credentials_path: str) -> str:
    """Returns the project id of the gcp service account used"""
    return load_json_file(gcp_credentials_path)["project_id"]


#############
# TEMPLATES #
#############

RCLONE_CONFIG_TEMPLATE = """
[s3]
type = s3
provider = AWS
env_auth = true
no_check_bucket = true
region = {REGION}

[gs]
type = google cloud storage
project_number = {GCP_PROJECT_ID}
service_account_file = {GCP_CRED_PATH}
"""
