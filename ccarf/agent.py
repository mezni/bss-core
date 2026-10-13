import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from a .env file
load_dotenv()

# Initialize the Anthropic client
client = Anthropic()

# Set the cheapest Haiku model
model = "claude-haiku-5-5"


def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text


# --- Example Usage ---
if __name__ == "__main__":
    conversation = []

    # Add a user message
    add_user_message(conversation, "My order #4821 has not arrived.")

    # Call chat with an optional system prompt
    reply = chat(conversation, system="Classify the ticket")
    print(f"Assistant: {reply}")

    # Save the assistant's reply back to history
    add_assistant_message(conversation, reply)
