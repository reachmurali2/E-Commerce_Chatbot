import os 
from groq import Groq
from dotenv import load_dotenv

load_dotenv() 

api_key = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=api_key)

def talk(query):
    prompt = f''' You are a helpful and friendly chatbot designed for small talk. You can answer questions about the weather, your name, your purpose, ans more. 

    QUESTION : {query}
    '''
    completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content" : prompt 
            }
        ],
        model = os.environ["GROQ_MODEL"]
    )
    return completion.choices[0].message.content