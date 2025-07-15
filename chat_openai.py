# chat_openai.py
import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def load_agent():
    model = OpenAIModel(
        model_name="gpt-4",  # or "gpt-3.5-turbo"
        provider=OpenAIProvider(api_key=None),  # Reads from OPENAI_API_KEY env var if None
    )
    return Agent(
        model=model,
        system_prompt="You are a helpful assistant. Keep answers concise and clear.",
    )

agent = load_agent()

st.title("🤖 OpenAI Chat Agent")
st.write("Ask anything to your OpenAI-powered assistant:")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["text"])

# Chat input
user_input = st.chat_input("Type your question...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Show loader while waiting for response
    with st.spinner("Thinking..."):
        response = agent.run_sync(user_input).output
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "text": response})
