from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a customer support assistant for an e-commerce "
            "store. Explain refund procedures clearly. Never claim "
            "that a refund has been approved or processed.",
        ),
        ("human", "{customer_message}"),
    ]
)

llm = ChatOpenAI(
    model="gpt-6-luna",
    #    temperature=0,
)

chain = prompt | llm


def ask_llm(customer_message: str) -> str:
    response = chain.invoke({"customer_message": customer_message})
    return str(response.content)
