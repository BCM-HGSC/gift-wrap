""" DynamoDB wrapper """
import logging
from typing import Dict

import boto3
from botocore.config import Config

from .constants import PROFILE_NAME

logger = logging.getLogger(__name__)


class DynamoDBResource:
    """Wrapper aroudn DynamoDBResource"""

    def __init__(self, table_name: str) -> None:
        config = Config(retries={"mode": "standard"})
        dynamodb = boto3.Session(profile_name=PROFILE_NAME).resource(
            "dynamodb", config=config
        )
        self.table = dynamodb.Table(table_name)

    def get_item(self, key: Dict):
        """Get state for DynamoDB item"""
        logger.info("Getting item from DynamoDB...")
        response = self.table.get_item(Key=key)
        return response.get("Item", {})

    def put_item(self, item: Dict):
        """Put item"""
        logger.info("Uploading item to DynamoDB...")
        return self.table.put_item(Item=item)

    def __repr__(self):
        return f"{self.__class__.__name__}(table: {self.table.name})"
