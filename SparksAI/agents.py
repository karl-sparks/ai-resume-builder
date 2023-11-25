"""Module Containing Agents used in AI Swarm"""
import logging
from typing import Literal, Optional, List
import openai

from langchain.tools import BaseTool
from langchain.tools.render import format_tool_to_openai_function
from langchain.chat_models import ChatOpenAI
from langchain.agents import OpenAIMultiFunctionsAgent
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)

from SparksAI import config
from SparksAI.memory import AIMemory
from SparksAI.swarm import Swarm

logger = logging.getLogger(__name__)

openai_client = openai.Client()

memory = AIMemory()

swarm = Swarm()


async def image_agent(prompt: str, style: Optional[Literal["vivid", "natural"]]) -> str:
    """Generate Image Agent

    Args:
        prompt (str): Prompt used to generate image
        style (str): The style of the generated images. Must be one of vivid or natural. Defaults to vivid.
                        Vivid causes the model to lean towards generating hyper-real and dramatic images
                        Natural causes the model to produce more natural, less hyper-real looking images.

    Returns:
        str: url to image generated
    """
    if len(prompt) > config.DALL_E_MAX_PROMPT_SIZE:
        return f"ValueError: Prompt size too large. Please try again with a prompt size less than {config.DALL_E_MAX_PROMPT_SIZE} characters."

    if not style:
        style = "vivid"

    if style not in ["vivid", "natural"]:
        return f"ValueError: Invalid value '{style}' for style. Please use either 'vivid' or 'natural' instead."

    logger.info("Generating %s image with prompt: %s", style, prompt)

    try:
        api_response = openai_client.images.generate(
            model=config.DALL_E_MODEL_NAME,
            prompt=prompt,
            style=style,
            size=config.DALL_E_SIZE,
            quality=config.DALL_E_QUALITY,
        )

        response = api_response.data[0].url
    except openai.OpenAIError as e:
        response = f"There was an error with image generation. Error Details:\n{e}"

    logger.info("Generated image: %s", response)

    return response


async def research_agent(prompt: str, username: str) -> dict:
    """Research Agent, will provide detailed info regarding a topic

    Args:
        prompt (str): Topics to research
        username (str): Username of questionor

    Returns:
        dict: returns two outputs. The first is analysis of previous interactions. The second is detailed review from an analyst.
    """
    convo_memory = memory.get_convo_mem(username=username).messages
    logger.info("Getting message summary")
    message_summary = await swarm.get_archivist(username).ainvoke(
        {"input_message": prompt, "memory": convo_memory}
    )

    logger.info("Getting Analyst Comments")
    analyst_review = await swarm.get_analyst_agent().ainvoke(
        {"content": f"Context: {message_summary}\n\nUser message: {prompt}"}
    )

    return {
        "prior_messages_analysis": message_summary.content,
        "analyst_review": analyst_review["output"],
    }


class DeciderAgent:
    """Currently not used; might use later if I move away from OpenAI's Assistant's API"""

    def __init__(self, tools: List[BaseTool]) -> None:
        raise NotImplementedError("Currently Not Implemented")

        self.tools = tools
        llm = ChatOpenAI(
            streaming=True, callbacks=FinalStreamingStdOutCallbackHandler()
        )

        self.llm = llm.bind_functions(
            [format_tool_to_openai_function(t) for t in self.tools]
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="""Your role is Tav, a processor of requests, tasked with identifying the most suitable agent to handle each request. You have two options:
    1. image_agent
        - Purpose: Creates images based on provided descriptions. 
        - Output: Delivers a link to the created image.
    
    2. research_agent
       - Purpose: Prepares research reports on specified topics.
       - Output: Provides a detailed report on the chosen research subject.
       
    If uncertain about which agent to engage, seek additional information to make an informed decision. However, if it's clear that the user will provide a follow-up message, you may wait for further clarification before responding. Your personality is characterized by stubbornness, curiosity, argumentativeness, and intelligence, traits reminiscent of the red-haired Sparks family who created you."""
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | self.llm
            | OpenAIFunctionsAgentOutputParser()
        )

        self.decider = OpenAIMultiFunctionsAgent(
            llm=self.llm,
            tools=self.tools,
        )
