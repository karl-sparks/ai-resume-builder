import polars as pl
from pydantic import BaseModel, constr, Field
from uuid import UUID, uuid4
from datetime import datetime
import os

DATA_FILE_PATH = "../data/chat_messages.parquet"


class ChatMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now)
    user: constr(min_length=1, max_length=20)
    message: constr(min_length=1, max_length=100)


def add_data_to_parquet(msg: ChatMessage) -> None:
    input_msg = pl.DataFrame(msg.model_dump()).with_columns(
        pl.col("id").map_elements(lambda x: str(x))
    )

    if os.path.exists(DATA_FILE_PATH):
        (
            pl.read_parquet(source=DATA_FILE_PATH)
            .vstack(input_msg)
            .write_parquet(file=DATA_FILE_PATH)
        )
    else:
        input_msg.write_parquet(file=DATA_FILE_PATH)


class database:
    def __init__(self) -> None:
        pass

    def create(self, msg: ChatMessage):
        return self
