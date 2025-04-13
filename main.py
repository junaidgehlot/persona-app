import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
client.api_key =  os.getenv("OPENAI_API_KEY") 

personalities = [personality.replace('.txt', '') for personality in os.listdir('scripts') if personality.endswith('.txt')]
messages=[]


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
    index = personalities.index(personality)       
    if index >= 0:
        f = open(f'scripts/{personalities[index]}.txt', "r")
        return f.read()
    
def add_chat_message(role, content):
    messages.append({'role':role,'content':content})   

    
def construct_persona_response():  
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": 'json_object'},
        messages = messages
    )
    return response    


def start(personality):  
    print("Start your chat")
    script= retrieve_persona_script(personality)
    add_chat_message('system',generate_personality_script(personality, script))
    while True:
        user_chat = input(f'Start chatting with {personality}')       
        add_chat_message('user',user_chat)       
        response = construct_persona_response()
        parsed_response = json.loads(response.choices[0].message.content)
        print(parsed_response.get('content'))
        if parsed_response.get('step') == 'end':
            break



start(personalities[0])
        



    



       







