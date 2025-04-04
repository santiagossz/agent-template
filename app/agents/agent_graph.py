import json
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from collections.abc import AsyncGenerator

from .agent import Agent, AgentState


class AgentGraph:
    def __init__(self):
        self.memory = MemorySaver()
        self.agent = Agent()
        self.graph = self._create_graph()

    def _create_graph(self):
        graph = StateGraph(AgentState)

        graph.add_node("router", self.agent.router)

        graph.set_entry_point("router")

        return graph.compile(checkpointer=self.memory)

    async def run_stream_workflow(self, state, config) -> AsyncGenerator[str, None]:  # type: ignore
        async for mode, msg in self.graph.astream(
            state, config, stream_mode=["custom", "messages"]
        ):
            if mode == "messages":
                chunk, metadata = msg
                yield json.dumps(
                    {"content": chunk.content, "node": metadata["langgraph_node"]}
                )
            else:
                yield json.dumps(msg)

    def get_memory(self, config):
        return self.graph.get_state(config).values
