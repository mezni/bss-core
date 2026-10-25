import logging
from collections.abc import Callable
from typing import Any

from langchain.agents.middleware import wrap_tool_call
from langchain.agents.middleware.types import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from pydantic import ValidationError

logger = logging.getLogger(__name__)


@wrap_tool_call
def handle_tool_errors(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]],
) -> ToolMessage | Command[Any]:
    """Never let a tool exception kill the run or leak internals to the model."""
    try:
        return handler(request)
    except ValidationError as exc:
        # The model sent bad arguments: let it see what is wrong and retry once.
        problems = "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors())
        content = f"Invalid arguments ({problems}). Fix them and try again."
    except Exception:
        logger.exception("tool %s failed", request.tool_call["name"])
        content = "The tool failed. Do not retry. Escalate to a human agent."
    return ToolMessage(content=content, tool_call_id=request.tool_call["id"])
