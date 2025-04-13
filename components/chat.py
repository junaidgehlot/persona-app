import streamlit as st

def render_chat(messages, personality):
    for message in messages:
        if message in messages:
            if message['role'] == 'user':
                st.markdown(f'<div class="user-messages" style="margin-bottom: 10px">You: {message['content']}</div>', unsafe_allow_html=True)
            elif  message['role'] != 'system':
                st.markdown(f'<div class="bot-messages" style="margin-bottom: 10px">{personality}: {message['content']}</div>', unsafe_allow_html=True)  