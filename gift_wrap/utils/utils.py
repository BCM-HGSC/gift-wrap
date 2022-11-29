import logging
import json
import subprocess
from typing import Dict
from pathlib import Path

logger = logging.getLogger(__name__)


def load_json_file(file_path) -> Dict[str, str]:
    """Reads a JSON file and returns its contents"""
    file_path = Path(file_path)
    with open(file_path, encoding="utf-8") as fin:
        return json.load(fin)


def subprocess_cmd(command):
    """Runs a subprocess command"""
    logging.info('Subprocess Command: "%s"', " ".join(command))
    return subprocess.run(command, check=True, capture_output=True, text=True)
