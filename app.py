import streamlit as st
from dotenv import load_dotenv
from components.chat import render_chat
from utils.message_handler import ( get_personalities, construct_persona_response, generate_personality_script, retrieve_persona_script)


# Load environment variables
load_dotenv()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_personality' not in st.session_state:
    st.session_state.current_personality = None

if 'initialized' not in st.session_state:
    st.session_state.initialized = False

if 'message_input' not in st.session_state:
        st.session_state.message_input = ""

# Define a callback function to handle personality selection change
def on_personality_change():
    # Clear message input when personality changes
    st.session_state.message_input = ""


def handle_submit():
    if st.session_state.message_input:
        user_message = st.session_state.message_input
    st.session_state.chat_history.append({
            'role': 'user',
            'content': user_message
        })
      # Get API response
    api_messages = [{'role': m['role'], 'content': m['content']} for m in st.session_state.chat_history]
    response = construct_persona_response(
        api_messages, 
        st.session_state.current_personality
    )
    
    # Add assistant response
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': response['content']
    })
    
    if response['step'] == 'end':
        st.session_state.conversation_ended = True
    
    # Clear the input (this will work because we're using callbacks)
    st.session_state.message_input = ""
    

# App title
st.title("AI Persona Chat")

personalities = get_personalities()

selected_personality = st.sidebar.selectbox(
    "Choose a personality to chat with:",
    personalities,
    key="selected_personality",
    on_change=on_personality_change

)



script = retrieve_persona_script(selected_personality)
if st.session_state.chat_history and not any(msg.get('role') == 'system' for msg in st.session_state.chat_history):
    st.session_state.chat_history.append({
            'role': 'system',
            'content':generate_personality_script(selected_personality, script)
        })

if st.sidebar.button("Start Chat") or st.session_state.current_personality != selected_personality:
    st.session_state.current_personality = selected_personality
    st.session_state.chat_history = []
    st.session_state.initialized = True
    st.success(f"Started a new chat with {selected_personality}!")

if st.session_state.current_personality:
    st.subheader(f"Chatting with: {st.session_state.current_personality}")

    render_chat(st.session_state.chat_history, selected_personality)
     # Show conversation ended message if applicable
    if st.session_state.get('conversation_ended', False):
        st.info("Conversation ended by the AI persona.")
    
    # Create the chat input with a form approach
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Type your message:", 
            key="message_input"
        )
        submit_button = st.form_submit_button("Send", on_click=handle_submit)
else:
    st.info("Please select a personality from the sidebar and click 'Start Chat'")



