from pydantic import BaseModel, Field


class UserDetails(BaseModel):
    """Model to contain user details"""

    username: str = Field(description="Username to find thread ID for")
    thread_id: str = Field(description="Thread ID for a given user")
