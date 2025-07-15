import streamlit as st
import logfire
from dataclasses import dataclass
import httpx

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

import os
from dotenv import load_dotenv

st.set_page_config(page_title="🤖 OpenAI Chat Agent", page_icon="🤖")


# Dataclass for storing API key and user name
@dataclass
class AppDeps:
    name: str
    api_key: str

# Create agent with deps_type for user info and api key
def get_agent(api_key):
    model = OpenAIModel(
        model_name="gpt-4o",
        provider=OpenAIProvider(api_key=api_key)
    )
    return Agent(
        model=model,
        deps_type=AppDeps,
    )


# Load environment variables from .env
load_dotenv()
agent = get_agent(os.getenv("OPENAI_API_KEY"))
logfire.configure()  
logfire.instrument_pydantic_ai()

# System prompt using user name
@agent.system_prompt
def get_system_prompt(ctx: RunContext[AppDeps]) -> str:
    return f"You are a helpful assistant. The user's name is {ctx.deps.name}. Personalize your answers."



# Only allow access if user is logged in
if "user_name" not in st.session_state or not st.session_state["user_name"]:
    st.warning("Please log in from the Login page before chatting.")
    st.stop()

st.title("🤖 OpenAI Chat Agent")
st.write("Ask anything to your OpenAI-powered assistant:")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["text"])

# Chat input
user_input = st.chat_input("Type your question...")



def get_response(user_input, user_name):
    api_key = os.environ.get("OPENAI_API_KEY")
    deps = AppDeps(name=user_name, api_key=api_key)
    result = agent.run_sync(user_input, deps=deps)
    return result.output

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})

    with st.spinner("Thinking..."):
        response = get_response(user_input, st.session_state.user_name)
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "text": response})
