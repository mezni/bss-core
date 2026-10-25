from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)

from refund_agent.reliability import retry_call

from refund_agent.intent import IntentResult

load_dotenv()

llm = ChatOpenAI(
    model="gpt-6-luna",
    #    temperature=0,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Classify the customer's e-commerce support request. "
            "Extract the order ID only when explicitly provided. "
            "Never invent missing information. Choose the closest "
            "allowed intent and refund reason. Return structured data.",
        ),
        ("human", "{customer_message}"),
    ]
)

chain = prompt | llm

intent_chain = prompt | llm.with_structured_output(IntentResult)


def ask_llm(customer_message: str) -> str:
    response = chain.invoke({"customer_message": customer_message})
    return str(response.content)


def extract_intent(customer_message: str) -> IntentResult:
    """Extract intent, retrying transient OpenAI API failures."""

    return retry_call(
        lambda: intent_chain.invoke({"customer_message": customer_message}),
        attempts=3,
        delay_seconds=0.5,
        retryable_exceptions=(
            APITimeoutError,
            APIConnectionError,
            RateLimitError,
            InternalServerError,
        ),
    )
