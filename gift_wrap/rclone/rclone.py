import subprocess
import logging
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional

from gift_wrap.utils.utils import subprocess_cmd
from . import exceptions

logger = logging.getLogger(__name__)


class RClone:
    """A wrapper around the rlcone class."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        self.config_path = config_path
        self._required_args = ["--checksum", "--error-on-no-transfer", "-vv"]

    def copy_to(self, source: str, dest: str, *args) -> CompletedProcess:
        """Uses rclone to copy file from GCP to s3"""
        command = self._initialize_command()
        command.extend(["copyto", source, dest, *self._required_args, *args])
        return self._submit_command(command)

    def copy_url(self, source: str, dest: str, *args) -> CompletedProcess:
        """Uses rclone to copy the contents of url to the given destination"""
        command = self._initialize_command()
        command.extend(["copyurl", source, dest, *self._required_args, *args])
        return self._submit_command(command)

    def _initialize_command(self) -> list[str]:
        """The first set of commands to occur before the user submitted ones."""
        command = ["rclone"]
        if self.config_path:
            command.extend(["--config", self.config_path])
        return command

    def _submit_command(self, command: list[str]) -> CompletedProcess:
        """Submits the rclone command with subprocess"""
        try:
            return subprocess_cmd(command)
        except subprocess.CalledProcessError as err:
            if "Unchanged skipping" in err.stderr:
                raise exceptions.FileAlreadyExist from err
            if "There was nothing to transfer" in err.stderr:
                raise exceptions.FileDoesNotExist from err
            raise exceptions.RCloneError(err.stderr or err.stdout) from err


def create_generic_config(working_dir: Path) -> str:
    """Creates a generic config for rclone. The default settings are to use
    GCP and AW2 environment variables."""
    config_path = working_dir / "intake-gvcf-tmp-rclone.conf"
    with open(config_path, "w", encoding="utf-8") as fout:
        fout.write(RCLONE_CONFIG_TEMPLATE)
    return str(config_path)


#############
# TEMPLATES #
#############

RCLONE_CONFIG_TEMPLATE = """
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
