from langchain_core.messages import ToolMessage

from refund_agent.llm import llm, prompt
from refund_agent.tools import lookup_order

tools = [lookup_order]
tools_by_name = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools)


def answer_with_tools(customer_message: str) -> str:
    messages = prompt.format_messages(customer_message=customer_message)

    for _ in range(5):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return str(response.content)

        for tool_call in response.tool_calls:
            tool = tools_by_name.get(tool_call["name"])

            if tool is None:
                messages.append(
                    ToolMessage(
                        content="Error: requested tool is unavailable.",
                        tool_call_id=tool_call["id"],
                    )
                )
                continue

            try:
                result = tool.invoke(tool_call["args"])
                content = str(result)
            except Exception:
                content = "Error: order lookup failed."

            messages.append(
                ToolMessage(
                    content=content,
                    tool_call_id=tool_call["id"],
                )
            )

    return "Unable to complete the request within the tool-call limit."
