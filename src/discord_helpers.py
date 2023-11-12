import logging

from discord import Client, TextChannel
from discord.errors import Forbidden

from src.big_query import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def load_historic_messages_into_database(client: Client):
    # Fetch history from guild channels
    logging.info("Checking Servers")
    for guild in client.guilds:
        for channel in guild.channels:
            if isinstance(channel, TextChannel):
                try:
                    async for message in channel.history(
                        limit=500
                    ):  # Adjust limit as needed
                        database.insert_row(message)
                except Forbidden:
                    logging.warning(
                        "Don't have permissions to read %s in %s",
                        channel.name,
                        guild.name,
                    )

    logging.info("Checking DMs")
    # Fetch history from DM channels
    for dm_channel in client.private_channels:
        if isinstance(dm_channel, discord.DMChannel):
            try:
                async for message in dm_channel.history(
                    limit=500
                ):  # Adjust limit as needed
                    database.insert_row(message)
            except discord.errors.Forbidden:
                logging.warning(
                    "Don't have permissions to read DM with %s", dm_channel.recipient
                )
