import uuid
from fastapi import APIRouter, Depends, HTTPException
from langchain_core.runnables import RunnableConfig
from typing import Annotated, Dict
from langgraph.types import Command
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from app.agents import AgentGraph, AgentState
from app.agents.vector_store.retriever import Retriever
from app.config.logging import logger

agent = AgentGraph()
graph = agent.graph

router = APIRouter()


class InputMessage(BaseModel):
    content: str
    content_type: str


async def get_config(session_id: str) -> RunnableConfig:
    return RunnableConfig(configurable={"thread_id": session_id})


Config = Annotated[RunnableConfig, Depends(get_config)]


@router.post("/session")
async def create_conversation():
    return {"session_id": str(uuid.uuid4())}


@router.post("/session/{session_id}/messages")
async def stream_conversation(input_msg: InputMessage, config: Config):  # type: ignore
    user_input = input_msg.content
    if input_msg.content_type == "text":
        logger.info(f"Starting Data Agent: {user_input}")
        state = AgentState(messages=user_input, data=[{}])
    else:
        state = Command(resume=user_input)
    return StreamingResponse(
        agent.run_stream_workflow(state, config),
        media_type="text/event-stream",
    )


@router.post("/session/{session_id}/memory")
async def memory(config: Config):  # type: ignore
    return agent.get_memory(config)


@router.post("/add_docs_vector_store")
async def add_docs_vector_store(collection: str, pdf: bool = True):
    try:
        retriever = Retriever(collection)
        return retriever.add_docs_to_vector_store()
    except Exception as e:
        raise HTTPException(500, f"Error while adding docs to vector store: {e}")
        ## add error handling


@router.post("/delete_docs_vector_store")
async def delete_docs_vector_store(collection: str, pdf: bool = True):
    try:
        retriever = Retriever(collection)
        retriever.vector_store._client.from_(collection).delete().neq(
            "content", None
        ).execute()
        return f"Successfully deleted docs from vector store {collection}"
    except Exception as e:
        raise HTTPException(500, f"Error while deleting docs from vector store: {e}")
