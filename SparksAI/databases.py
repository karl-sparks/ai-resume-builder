import logging
from typing import Optional, List
import os

from abc import ABC, abstractmethod
from google.cloud import bigquery, firestore
from google.api_core.exceptions import BadRequest

from dotenv import load_dotenv

from SparksAI.models import UserDetails

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


# Abstract base class for all database strategies
class DatabaseStrategy(ABC):
    @abstractmethod
    def insert_row(self, row: UserDetails) -> bool:
        """
        Method to insert a row into the database.

        Args:
            row (ThreadIDRecord): The row to be inserted.

        Returns:
            bool: True if the row was successfully inserted, False otherwise.
        """
        pass

    @abstractmethod
    def get_row_by_username(self, username: str) -> UserDetails:
        """
        Retrieves a ThreadIDRecord object corresponding to the provided username.

        Parameters:
            username (str): The username for which to retrieve the ThreadIDRecord.

        Returns:
            ThreadIDRecord: The ThreadIDRecord object corresponding to the provided username.
        """
        pass

    def get_all_rows(self) -> List[UserDetails]:
        """
        Get all rows from the database and return a list of UserDetails objects.

        :return: A list of UserDetails objects.
        :rtype: List[UserDetails]
        """
        pass

    @abstractmethod
    def delete_row_by_username(self, username: str) -> bool:
        """
        Deletes a row from the table by the given ID.

        Parameters:
            username (str): The ID of the row to delete.

        Returns:
            bool: True if the row was successfully deleted, False otherwise.
        """
        pass


# Concrete class for BigQuery strategy
class BigQueryStrategy(DatabaseStrategy):
    def __init__(self, table_id: str):
        """
        Initializes a new instance of the class.

        Args:
            table_id (str): The ID of the bigquary table to access.
        """
        self.client = bigquery.Client()
        self.table_id = table_id

    def insert_row(self, row: UserDetails) -> bool:
        """
        Inserts a row into the table.

        Args:
            row (ThreadIDRecord): The row to be inserted.

        Returns:
            bool: True if the row was inserted successfully, False otherwise.
        """
        errors = self.client.insert_rows_json(self.table_id, [row.model_dump()])

        if errors:
            logger.error("Encountered errors while inserting rows: %s", errors)
            return False
        else:
            logger.info("Row inserted successfully.")
            return True

    def get_row_by_username(self, username: str) -> Optional[UserDetails]:
        query = f"""
            SELECT *
            FROM `{self.table_id}`
            WHERE username = @username
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("username", "STRING", username)
            ]
        )
        query_job = self.client.query(query, job_config=job_config)
        result = [UserDetails(**row) for row in query_job]
        if len(result) == 1:
            logger.info("Retrieved user details for %s", username)
            return result[0]

        logger.warning("Failed to find user details for %s", username)
        return None

    def get_all_rows(self) -> Optional[List[UserDetails]]:
        query = f"""
            SELECT *
            FROM `{self.table_id}`"""

        query_job = self.client.query(query)
        result = [UserDetails(**row) for row in query_job]

        if result:
            logger.info("Retrieved all user details")
            return result

        logger.warning("Failed to find user details")
        return None

    def delete_row_by_username(self, username: str) -> bool:
        query = f"""
            DELETE FROM `{self.table_id}`
            WHERE username = @username
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("username", "STRING", username)
            ]
        )

        try:
            query_job = self.client.query(
                query, job_config=job_config
            )  # Make an API request.
            query_job.result()  # Wait for the job to complete.
            logger.info("User details successfully deleted for user: %s", username)
            return True

        except BadRequest as e:
            logger.warning(
                "Failed to delete details for user: %s, with error %s",
                username,
                str(e),
            )
            return False


class FireBaseStrategy(DatabaseStrategy):
    def __init__(self, collection_name: str):
        self.client = firestore.Client()
        self.collection_name = collection_name

    def insert_row(self, row: UserDetails) -> bool:
        doc_ref = self.client.collection(self.collection_name).document(
            str(row.user_id)
        )
        doc_ref.set(row.model_dump())
        logger.info("Row inserted successfully: %s", row.user_id)
        return True

    def get_row_by_username(self, username: str) -> Optional[UserDetails]:
        docs = (
            self.client.collection(self.collection_name)
            .where(field_path="discord_user_name", op_string="==", value=username)
            .stream()
        )
        for doc in docs:
            return UserDetails(**doc.to_dict())
        return None

    def get_all_rows(self) -> Optional[List[UserDetails]]:
        docs = self.client.collection(self.collection_name).stream()
        result = [UserDetails(**doc.to_dict()) for doc in docs]
        if result:
            logger.info("Retrieved all user details")
            return result
        logger.warning("Failed to find user details")
        return None

    def delete_row_by_username(self, username: str) -> bool:
        docs = (
            self.client.collection(self.collection_name)
            .where(field_path="discord_user_name", op_string="==", value=username)
            .stream()
        )
        for doc in docs:
            doc.reference.delete()
        logger.info("User details successfully deleted for user: %s", username)
        return True


# Database context that utilizes the strategy
class DatabaseContext:
    def __init__(self, strategy: DatabaseStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DatabaseStrategy):
        self._strategy = strategy

    def insert_row(self, row: UserDetails) -> bool:
        return self._strategy.insert_row(row)

    def get_row_by_username(self, username: str) -> Optional[UserDetails]:
        return self._strategy.get_row_by_username(username)

    def get_all_rows(self) -> Optional[List[UserDetails]]:
        return self._strategy.get_all_rows()

    def delete_row_by_username(self, username: str) -> bool:
        return self._strategy.delete_row_by_username(username)
