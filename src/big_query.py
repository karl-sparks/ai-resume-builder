import logging
from discord.message import Message
from abc import ABC, abstractmethod
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
from typing import Dict, Any
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


def message_to_dict(message):
    # Extracts the necessary information from the Discord Message object
    # and formats it to match the provided BigQuery schema.

    # Assuming 'message' is a discord.Message object
    # and 'message.attachments' is a list of discord.Attachment objects
    # For attachments, we're taking just the first one's URL for this example.
    return {
        "message_id": str(message.id),
        "channel_id": str(message.channel.id),
        "author_id": str(message.author.id),
        "author_name": message.author.name,
        "server_id": str(message.guild.id) if message.guild else "",
        "message_created_at": message.created_at.isoformat(),
        "message_content": message.content if message.content else "",
        "message_reactions": [str(reaction) for reaction in message.reactions]
        if message.reactions
        else "",
        "attachment_id": message.attachments[0].id if message.attachments else "",
    }


# Abstract base class for all database strategies
class DatabaseStrategy(ABC):
    @abstractmethod
    def insert_row(self, data: Message) -> None:
        pass

    @abstractmethod
    def get_row_by_id(
        self, id_value: str, id_name: str = "message_id"
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def delete_row_by_id(self, id_value: str, id_name: str = "message_id") -> None:
        pass

    @abstractmethod
    def get_all_rows(self) -> Dict[str, Any]:
        pass


# Concrete class for BigQuery strategy
class BigQueryStrategy(DatabaseStrategy):
    def __init__(self, table_id: str):
        self.client = bigquery.Client()
        self.table_id = table_id

    def insert_row(self, data: Message) -> None:
        insert_data = message_to_dict(data)

        errors = self.client.insert_rows_json(self.table_id, [insert_data])

        if errors:
            logger.error("Encountered errors while inserting rows: %s", errors)
        else:
            logger.info("Row inserted successfully.")

    def get_row_by_id(
        self, id_value: str, id_name: str = "message_id"
    ) -> Dict[str, Any]:
        query = f"""
            SELECT *
            FROM `{self.table_id}`
            WHERE {id_name} = @id_value
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("id_value", "STRING", id_value)
            ]
        )
        query_job = self.client.query(query, job_config=job_config)
        result = [dict(row.items()) for row in query_job]
        if result:
            logger.info("Retrieved row with %s = %s.", id_name, id_value)
            return result
        else:
            logger.warning("No row found with %s = %s.", id_name, id_value)
            return None

    def delete_row_by_id(self, id_value: str, id_name: str = "message_id") -> None:
        query = f"""
            DELETE FROM `{self.table_id}`
            WHERE {id_name} = @id_value
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("id_value", "STRING", id_value)
            ]
        )

        try:
            query_job = self.client.query(
                query, job_config=job_config
            )  # Make an API request.
            query_job.result()  # Wait for the job to complete.
            logger.info("Row with %s = %s deleted successfully.", id_name, id_value)

        except BadRequest as e:
            logger.error("Error deleting row: %s", e)

    def get_all_rows(self) -> Dict[str, Any]:
        query = f"""SELECT * FROM `{self.table_id}`"""

        query_job = self.client.query(query)
        result = [dict(row.items()) for row in query_job]
        if result:
            logger.info("Retrieved all rows")
            return result
        else:
            logger.warning("No rows found")
            return None


# Database context that utilizes the strategy
class DatabaseContext:
    def __init__(self, strategy: DatabaseStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DatabaseStrategy):
        self._strategy = strategy

    def insert_row(self, data: Message):
        self._strategy.insert_row(data)

    def get_row_by_id(self, id_value: str, id_name: str = "message_id"):
        return self._strategy.get_row_by_id(id_value, id_name)

    def delete_row_by_id(self, id_value: str, id_name: str = "message_id"):
        self._strategy.delete_row_by_id(id_value, id_name)

    def get_all_rows(self):
        return self._strategy.get_all_rows()


# Usage
table_id_str = os.getenv("BIGQUERY_TABLE_ID")
bigquery_strategy = BigQueryStrategy(table_id=table_id_str)

database = DatabaseContext(strategy=bigquery_strategy)
