from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_llm():
    return init_chat_model(model="gpt-6-luna")
