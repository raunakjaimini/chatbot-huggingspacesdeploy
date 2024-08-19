import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat-Mate",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "bot"
    else:
        return "user"

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("Chat-Mate Gemini Version")

# Function to display messages with custom labels
# def display_message(role, message):
#     if role == "user":
#         st.markdown(f"**User**: {message}")
#     else:
#         st.markdown(f"**Chat-Mate**: {message}")
def display_message(role, message):
    if role == "user":
        st.markdown(f'<div style="color: grey; padding: 10px; margin: 5px; border-radius: 5px; border: 1px solid grey;"><b>User:</b> {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color: white ; padding: 10px; margin: 5px; border-radius: 5px; border: 1px solid white;"><b>Bot:</b> {message}</div>', unsafe_allow_html=True)


# Display the chat history
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    display_message(role, message.parts[0].text)

# Input field for user's message
user_prompt = st.text_input("Ask anything....")
if user_prompt:
    # Add user's message to chat and display it
    display_message("user", user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    display_message("bot", gemini_response.text)
