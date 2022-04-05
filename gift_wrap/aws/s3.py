""" S3 Wrapper """
import logging
from pathlib import Path
from typing import Iterator, Tuple

import boto3
from mypy_boto3_s3.service_resource import ObjectSummary
from botocore.config import Config
from yarl import URL

from gift_wrap.utils.cloud_service import CloudService
from .constants import PROFILE_NAME
from .exceptions import NotAnS3Uri

logger = logging.getLogger(__name__)


class S3Resource(CloudService):
    """S3Resource wrapper"""

    def __init__(self, bucket_name: str) -> None:
        config = Config(retries={"mode": "standard"})
        self.bucket_name = bucket_name

        self.resource = boto3.Session(profile_name=PROFILE_NAME).resource(
            "s3", config=config
        )

    def delete_file(self, remote_file: str) -> None:
        """
        Given a file name, deletes the object from the given bucket.

        Args:
            file_name (str): Name of the remote S3 object.
        """
        logger.info("S3: Deleting %s from %s", remote_file, self.bucket_name)
        self.resource.Object(self.bucket_name, remote_file).delete()

    def download_file(self, remote_file: str, destination: str, **kwargs) -> None:
        """
        Given a file name, downloads the object from the given bucket to the
        given destination.

        Args:
            file_name (str): Name of the remote S3 object.
            destination (str): The str local path where the remote file will be
                downloaded to.
        """
        logger.info("S3: Downloading %s from %s", remote_file, self.bucket_name)
        obj = self.resource.Object(self.bucket_name, remote_file)
        obj.download_file(destination, **kwargs)

    def list_files(self, prefix: str, **kwargs) -> Iterator[ObjectSummary]:
        """
        Given a bucket name and a prefix to list_files,
        returns an iterator of S3 ObjectSummary.

        Args:
            prefix (str): The prefix in which to filter the bucket.

        Return:
            An iterator of S3 ObjectSummary.
        """
        logger.info("S3: Getting objects from %s", prefix)
        bucket = self.resource.Bucket(self.bucket_name)
        return bucket.objects.filter(Prefix=prefix, **kwargs)

    def upload_file(self, local_file: str, destination: str) -> None:
        """
        Creates an object at the given s3 bucket.

        Args:
            local_path (Path): The local path of the file to upload.
            file_name (str): The name of the object where the file will be
                uploaded to.
        """
        logger.info("S3: Uploading file %s to %s", local_file, destination)
        obj = self.resource.Object(self.bucket_name, destination)
        obj.upload_file(
            Filename=local_file,
        )

    def upload_dir_to_bucket(self, prefix: str, dir_path: Path) -> None:
        """
        Given a pathlib Path of a directory, creates the directory and uploads
        its contents to the designated bucket_name.

        Note: S3 does not have 'folder' concepts In reality its just prefix.

        Args:
            prefix (str): The prefix in which the directory should be uploaded
                to. In this case, the prefix acts a remote directory in S3.
            dir_path (Path): The local directory to be uploaded
        """
        logger.info("S3: Uploading directory %s...", dir_path)
        for file in dir_path.rglob("*"):
            if file.is_file():
                file_name = f"{prefix}/{dir_path.stem}/{file.name}"
                self.upload_file(
                    str(file),
                    file_name,
                )
        logger.info("S3: Directory uploaded to S3.")


#########
# Utils #
#########
def get_bucket_and_key_from_s3uri(uri: str) -> Tuple[str, str]:
    """
    Given an S3 URI string: s3://bucket_name/key/to/file.jpg,
    the method will return the bucket_name and the key (in this case),
    key/to/file.jpg
    """
    uri = URL(uri)
    if uri.scheme != "s3":
        raise NotAnS3Uri("string is not expected s3")
    return uri.host, uri.raw_path[1:]


def prefix_check(prefix: str) -> str:
    """
    Verifies that a given prefix does not start with '/'.
    """
    return prefix[1:] if prefix[0] == "/" else prefix
