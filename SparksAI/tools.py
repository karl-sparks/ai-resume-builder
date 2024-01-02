"""Module containing tools for OpenAI Assistents to use"""
from typing import Type, Optional
import logging

from pydantic import BaseModel, Field

from langchain.tools import BaseTool

from SparksAI import agents


logger = logging.getLogger(__name__)


class ImageAgentInput(BaseModel):
    """Input for image_agent"""

    prompt: str = Field(
        description="Prompt used to generated image. Should be as detailed as possible."
    )
    style: Optional[str] = Field(
        description="The style of the generated images. Must be one of vivid or natural. Vivid causes the model to lean towards generating hyper-real and dramatic images. Natural causes the model to produce more natural, less hyper-real looking images."
    )


class ImageAgentTool(BaseTool):
    """Tool for OpenAI Assistant to use the image generation agent"""

    name = "image_agent"
    description = "Used to generate an image based on a prompt. The prompt should be as detailed as possible. It will return the url to the image."

    args_schema: Type[BaseModel] = ImageAgentInput

    def _run(self, prompt: str, style: str) -> str:
        id_run = "unknown_run"
        logger.info("%s : Running Image Agent sync : %s : %s", id_run, prompt, style)
        return agents.image_agent(prompt, style)

    async def _arun(self, prompt: str, style: str) -> str:
        id_run = "unknown_run"
        logger.info("%s : Running Image Agent async : %s : %s", id_run, prompt, style)
        return await agents.image_agent(prompt, style)


class ResearchAgentInput(BaseModel):
    """Input for research_agent"""

    prompt: str = Field(
        description="Topic for agent to research. Should be target to provide information needed to answer users question."
    )
    username: str = Field(
        description="Username of user asking questions. This is used to provide context and analysis on previous user interactions."
    )


class ResearchAgentTool(BaseTool):
    """Tool for OpenAI Assistant to use the research agent"""

    name = "research_agent"
    description = "Used to generate a research report on a topic. The topic should be as detailed as possible and targeted to answer the users questions."

    args_schema: Type[BaseModel] = ResearchAgentInput

    def _run(self, prompt: str, username: str) -> str:
        id_run = "unknown_run"
        logger.info(
            "%s : Running Research Agent sync  : %s : %s", id_run, prompt, username
        )
        response = agents.research_agent(prompt, username)
        return str(response)

    async def _arun(self, prompt: str, username: str) -> str:
        id_run = "unknown_run"
        logger.info(
            "%s : Running Research Agent async : %s : %s", id_run, prompt, username
        )
        response = await agents.research_agent(prompt, username)
        return str(response)
