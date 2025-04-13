import streamlit as st
from components.chat import render_chat
from utils.message_handler import load_chat_history, save_message


# Initialize the Streamlit app
st.title("Persona app")

chat_history = load_chat_history()

# Display chat interface
render_chat(chat_history)

# Input for new messages
user_input = st.text_input("Type your message:")


if st.button("Send"):
    if user_input:
        # Save the new message
        save_message(user_input)
        st.experimental_rerun()  # Refresh the app to show the new message