import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",
    layout="wide",
)

# Set your Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("🚨 GOOGLE_API_KEY is not set. Please check your .env file.")
    st.stop()

# Configure Google Generative AI
try:
    gen_ai.configure(api_key=GOOGLE_API_KEY)
    model = gen_ai.GenerativeModel("gemini-1.5-pro")  # ✅ Correct model name
except Exception as e:
    st.error(f"Error loading Gemini Pro model: {e}")
    st.stop()

# Role translation for Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# App title
st.title("🤖 wiskey Pro - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Chat input
user_prompt = st.chat_input("Ask wiskey...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    except Exception as e:
        st.error(f"Gemini Pro failed to respond: {e}")
