from langgraph.graph import MessagesState
from langgraph.types import Command  # , interrupt
from typing import Literal
from enum import StrEnum
from langgraph.types import StreamWriter
from pydantic import BaseModel, Field

from .llm import llm_provider
from app.config.logging import logger
from .prompts import PromptGenerator


class Routes(StrEnum):
    pass


class Nodes(StrEnum):
    pass


route_options = Literal[*[route.value for route in Routes]]  # type: ignore


class Router(BaseModel):
    route: route_options = Field(description="The route to take")  # type: ignore
    fallback: str = Field(description="The agent response to the user")


class DataAgentState(MessagesState):
    pass


class Agent:
    def __init__(self):
        self.lp = llm_provider()
        self.pg = PromptGenerator

    async def router(self, state, writer: StreamWriter) -> Command[route_options]:  # type: ignore
        logger.info("-------------- Routing Data Agent --------------")
        router_llm = self.lp.llm_no_streaming.with_structured_output(Router)
        prompt = self.pg.router(state)
        response = await router_llm.ainvoke(prompt)
        goto = response.route
        writer({"node": "router", "content": response.fallback})
        if goto == Routes.END:
            logger.info("-------------- Ending Data Agent --------------")
            return Command(goto=goto, update={"messages": response.fallback})
        return Command(goto=goto)
