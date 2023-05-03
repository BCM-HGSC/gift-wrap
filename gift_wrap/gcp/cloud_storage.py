"""Interfacing with Google Cloud Platform."""
import logging
from typing import Iterator

from google.cloud import storage

from gift_wrap.utils.cloud_service import CloudService

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 60


class StorageClient(CloudService):
    """Wrapper for GCP Client"""

    def __init__(self, bucket_name: str) -> None:
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket_name)

    def delete_file(self, remote_file: str) -> None:
        """
        Given a blob name, delete the blob from the set bucket.

        Args:
            remote_file (str): The name of the Blob in the Bucket.
        """
        blob = self.bucket.blob(remote_file)
        blob.delete()

    def download_file(self, remote_file: str, destination: str, **kwargs) -> None:
        """
        Downloads a blob from the Google Bucket.

        Args:
            key (str): The key string of the GCP Blob.
            destination (str or Path): The destination in which the blob will be
                downloaded to.
            timeout (int): The number of seconds to wait for server response.
                The default is 60.
            checksum (str): The type of checksum to generate.

        """
        blob = self.bucket.blob(remote_file)
        blob.download_to_filename(destination, **kwargs)

    def list_files(self, prefix: str, **kwargs) -> Iterator[storage.Blob]:
        """
        Returns an iterator of `google.cloud.storage.Blob` that match the
        given prefix.

        Args:
            prefix (str): Prefix used to filter blobs.
            delimiter (str): (Optional) Delimiter, used with ``prefix`` to
                emulate hierarchy.

        Returns:
            Iterator of all `google.cloud.storage.blob.Blob` in the bucket
            matching the arguments.

        """
        return self.client.list_blobs(self.bucket, prefix=prefix, **kwargs)

    def upload_file(self, local_file: str, destination: str) -> None:
        """
        Uploads a file to the set bucket.

        Args:
            local_file (str): The path to the file.
            destination (str): The name of the blob to be instantiated.
        """
        logger.info("GCP: Uploading file %s to GCP.", local_file)
        blob = self.bucket.blob(destination)
        blob.upload_from_filename(local_file)


def fix_prefix(prefix):
    """
    If a GCP prefix doesn't end with "/", add it.
    """
    prefix = str(prefix)
    if prefix[-1] != "/":
        return f"{prefix}/"
    return prefix
