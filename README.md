# Persona Chat App

Demo Url: https://personademo.streamlit.app/

A streamlit-based application that allows users to chat with AI personas mimicking different personalities based on script samples.

## Project Overview

This application creates an interactive chat experience where users can select from various personalities (currently Hitesh and Piyush) and engage in conversation with AI personas that mimic their speaking style. The application uses the OpenAI GPT-4o model to generate responses that maintain the tone and style of the selected personality.

## Features

- Select from multiple personalities to chat with
- AI responses mimic the speaking style and tone of the selected personality


 Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/persona-app.git
   cd persona-app
   pip install -r requirements.txt

2. Create a .env file in the root directory with your OpenAI API key:
   OPENAI_API_KEY=your_api_key_here
    ```bash
    streamlit run app.py

1. Select a personality from the sidebar dropdown
2. Click "Start Chat" to begin a conversation
3. Type your message in the input box and click "Send"
4. The AI will respond in the style of the selected personality
5. The conversation ends when you type "bye" or a similar ending phrase
