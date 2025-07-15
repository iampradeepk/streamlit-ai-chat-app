# chat_app.py
import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.providers.bedrock import BedrockProvider

# Cached agent to prevent reinitializing on every rerun
@st.cache_resource
def load_agent():
    model = BedrockConverseModel(
        model_name="amazon.titan-chat-preview:1.0",  # Replace with your model
        provider=BedrockProvider(region_name="us-east-1"),
    )
    return Agent(model=model, system_prompt="You are a helpful assistant.")

agent = load_agent()

# Streamlit UI
st.title("💬 Bedrock Chat Agent")
st.write("Ask anything to your Bedrock-powered agent:")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["text"])

# Input box
user_input = st.chat_input("Type your question here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Get agent response
    response = agent.run_sync(user_input).output
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "text": response})
