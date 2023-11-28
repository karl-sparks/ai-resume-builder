import os

from langchain.memory import FileChatMessageHistory

from SparksAI import databases
from SparksAI.models import UserDetails


class AIMemory:
    def __init__(self) -> None:
        self._convo_mem = {}
        self._user_details = {}

        # initialise db
        bigquery_strategy = databases.BigQueryStrategy(
            table_id=os.getenv("BIGQUERY_USER_DETAILS_TALBE_ID")
        )

        self._db = databases.DatabaseContext(strategy=bigquery_strategy)

        users = self._db.get_all_rows()

        for user in users:
            self._user_details[user.username] = user

    def get_convo_mem(self, username: str) -> FileChatMessageHistory:
        if username in self._convo_mem:
            return self._convo_mem[username]

        else:
            self._convo_mem[username] = FileChatMessageHistory(f"{username}_memory.txt")

            return self._convo_mem[username]

    def reterive_user_thread_id(self, username: str) -> str:
        if username in self._user_details:
            return self._user_details[username].thread_id

        return self._db.get_row_by_username(username).thread_id

    def update_user_details(self, username: str, thread_id: str) -> None:
        self._user_details[username] = UserDetails(
            username=username, thread_id=thread_id
        )
        self._db.insert_row(self._user_details[username])

    def update_db(self) -> None:
        for _, user in self._user_details.items():
            self._db.insert_row(user)
