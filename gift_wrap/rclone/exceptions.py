from dataclasses import dataclass


@dataclass
class FileAlreadyExist(Exception):
    """Raised when a file given already exist at the given destination"""

    msg: str = "File already exist at the given destination."


@dataclass
class FileDoesNotExist(Exception):
    """Source file does not exist."""

    msg: str = "Source file does not exist."


@dataclass
class RCloneError(Exception):
    """A generic RClone Error raised whenever unable to copy a file."""

    message: str
