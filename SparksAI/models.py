from pydantic import BaseModel, Field
from uuid import uuid4


class UserDetails(BaseModel):
    """Model to contain user details"""

    user_id: str = Field(
        description="Unique ID of user", default_factory=lambda: str(uuid4())
    )
    discord_user_name: str = Field(description="User name on discord")
    thread_id: str = Field(description="Thread ID for a given user")
