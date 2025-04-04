from langchain_openai import ChatOpenAI
from functools import lru_cache
from app.config import agent_cfg


@lru_cache()
def llm_provider():
    return LLMProvider()


class LLMProvider:
    def __init__(self):
        self._llm = ChatOpenAI(model=agent_cfg.OPENAI_MODEL)
        self._llm_mini = ChatOpenAI(model=agent_cfg.OPENAI_MODEL_MINI)
        self._llm_no_streaming = ChatOpenAI(
            model=agent_cfg.OPENAI_MODEL, disable_streaming=True
        )

    @property
    def llm(self):
        """Main LLM instance"""
        return self._llm

    @property
    def llm_mini(self):
        """Mini LLM instance"""
        return self._llm_mini

    @property
    def llm_no_streaming(self):
        """Non-streaming LLM instance"""
        return self._llm_no_streaming

    @property
    def llm_tools(self, tools):
        """Get the main LLM with tools bound to it"""
        return self._llm_no_streaming.bind_tools(tools)
