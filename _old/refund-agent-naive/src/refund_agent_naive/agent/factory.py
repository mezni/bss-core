from typing import Any

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from refund_agent_naive.agent.middleware import handle_tool_errors
from refund_agent_naive.config import Settings
from refund_agent_naive.context import AgentContext
from refund_agent_naive.prompts import load_prompt
from refund_agent_naive.services.refund_service import RefundService
from refund_agent_naive.tools.refund_tools import build_refund_tools

PROMPT_NAME = "refund_agent.v1"


def build_chat_model(settings: Settings) -> BaseChatModel:
    return init_chat_model(
        settings.model_name,
        api_key=settings.openai_api_key.get_secret_value(),
        timeout=settings.llm_timeout_s,
        max_retries=settings.llm_max_retries,
        temperature=0,
    )


def build_agent(
    model: BaseChatModel,
    service: RefundService,
    checkpointer: BaseCheckpointSaver[Any],
) -> CompiledStateGraph[Any, Any, Any, Any]:
    return create_agent(
        model=model,
        tools=build_refund_tools(service),
        system_prompt=load_prompt(PROMPT_NAME),
        middleware=[handle_tool_errors],
        context_schema=AgentContext,
        checkpointer=checkpointer,
    )


def run_config(thread_id: str, settings: Settings) -> RunnableConfig:
    """Per-run config. One model call plus one tool call is two graph steps,
    so allow 2 * max_agent_steps + 1."""
    return {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 2 * settings.max_agent_steps + 1,
    }
