""" Generic class for CRUD cloud services to inherit """
from abc import ABC, abstractmethod
from typing import Any, Iterator


class CloudService(ABC):
    """General cloud client"""

    @abstractmethod
    def list_files(self, prefix: str, **kwargs) -> Iterator[Any]:
        """Gets files under the given prefix"""

    @abstractmethod
    def upload_file(self, local_file: str, destination: str):
        """Uploads a file"""

    @abstractmethod
    def delete_file(self, remote_file: str) -> None:
        """Deletes a file"""

    @abstractmethod
    def download_file(self, remote_file: str, destination: str, **kwargs) -> None:
        """Downloads an object"""
