""" DynamoDB wrapper """
import logging
from typing import Dict

import boto3
from botocore.config import Config
from mypy_boto3_dynamodb.type_defs import UpdateItemInputRequestTypeDef

logger = logging.getLogger(__name__)


class DynamoDBResource:
    """Wrapper around DynamoDBResource"""

    def __init__(self, table_name: str) -> None:
        config = Config(retries={"mode": "standard"})
        dynamodb = boto3.Session().resource("dynamodb", config=config)
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

    def update_item(self, item: UpdateItemInputRequestTypeDef):
        """Updates an item in DynamoDB"""
        logger.debug("Updating item: %s in DynamoDB...", item)
        return self.table.update_item(**item)

    def __repr__(self):
        return f"{self.__class__.__name__}(table: {self.table.name})"
