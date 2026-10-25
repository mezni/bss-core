from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()


llm = ChatOpenAI(model="gpt-6-luna")

agent = create_agent(
    model=llm,
)
