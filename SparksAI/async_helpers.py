"""Module containing code to deal with async"""
from collections.abc import AsyncIterator, Awaitable


class AreturnMessageIterator(AsyncIterator):
    """
    It is currently used as a temporary solution to convert non-streamed output into streamed output.
    This approach allows me to avoid reimplementing the message-sending functionality and use the Assistant
    API before the streaming feature is implemented.
    """

    def __init__(self, message: str, chunk_size: int):
        if not isinstance(message, str):
            raise ValueError(f"Message must be a str: {message}")

        self.index = 0
        self.msg = message
        self.chunk_size = chunk_size

    async def __anext__(self) -> Awaitable:
        if self.index < len(self.msg):
            end = min(self.index + self.chunk_size, len(self.msg))
            chunk = self.msg[self.index : end]
            self.index = end

            return chunk
        else:
            raise StopAsyncIteration
