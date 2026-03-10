import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key safely
api_key = os.getenv("G")

if not api_key:
    st.error("⚠️ Groq API key not found. Please set environment variable 'G'.")
    st.stop()

# Initialize client
client = Groq(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="centered"
)

# Sidebar settings
with st.sidebar:
    st.title("⚙️ Settings")

    model = st.selectbox(
        "Choose Model",
        ["llama-3.1-8b-instant"]
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.chat = []
        st.rerun()

    st.markdown("---")
    st.write("Simple LLM Chat App")
    st.write("Powered by Groq + Streamlit")

# Main title
st.title("🤖 AI Chat Assistant")
st.markdown("Ask anything and get AI responses instantly.")

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat history
for message in st.session_state.chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your message...")

if prompt:

    # Store user message
    st.session_state.chat.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):

            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.chat
            )

            reply = response.choices[0].message.content

            st.markdown(reply)

    # Store assistant response
    st.session_state.chat.append(
        {"role": "assistant", "content": reply}
    )
