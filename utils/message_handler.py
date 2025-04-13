import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
client.api_key =  os.getenv("OPENAI_API_KEY") 

os.makedirs('data', exist_ok=True)
CHAT_HISTORY_FILE = 'data/chat_history.json'
PERSONALITIES_DIR = 'scripts'

personalities = [personality.replace('.txt', '') for personality in os.listdir(PERSONALITIES_DIR) if personality.endswith('.txt')]


def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []
    with open(CHAT_HISTORY_FILE, 'r') as f:
        return json.loads()
    
def save_message(content, role="user"):
    chat_history = load_chat_history()
    chat_history.append({'role': role, 'content':content})

    with open(CHAT_HISTORY_FILE, 'w')  as f:
        json.dumps(chat_history, f)
    return chat_history
    
def get_personalities():
    return  [personality.replace('.txt', '') for personality in os.listdir(PERSONALITIES_DIR) if personality.endswith('.txt')]


def generate_personality_script(personality, script):
    return  f"""
        You are playing a role of {personality},

        Below is the script that provides this person
        {{script: {script}}}

        Important:
        Do not extract any contextual meaning from the script, It is meant to be use for tone and style

        Rules:
        1. follow thw strict JSON output as per output schema
        
        Output Format:
        {{step: 'string', content: "string"}}   

        Example:
        Input: Hi
        Output:{{step: "reply", content: {personality} response}}

        Example:
        Input: bye
        Output:{{step: "end", content: {personality} respose}}
    """


def retrieve_persona_script(personality):
    personalities = get_personalities()
    if personality in personalities:
        with open(f'{PERSONALITIES_DIR}/{personality}.txt', "r") as f:
            return f.read()

    
def construct_persona_response(messages, personality):  
    script = retrieve_persona_script(personality)
    if not any(msg.get('role') == 'system' for msg in messages):
        system_message = {
            'role': 'system',
            'content': generate_personality_script(personality, script)
        }
        messages.append(system_message)

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": 'json_object'},
        messages = messages
    )
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)
        
        



    



       







