import streamlit as st

st.set_page_config(page_title="Login", page_icon="🔑")

st.title("Login")
user_name = st.text_input("Enter your name to start chatting:")

if user_name:
    st.session_state.user_name = user_name
    st.success("Login successful! Go to the Chat page to start chatting.")
    # Optionally, you can auto-redirect:
    st.switch_page("pages/chat_openai.py")
