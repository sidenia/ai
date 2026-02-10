from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0, # Adjust the temperature as needed for more or less creativity
        openai_api_key=OPENAI_API_KEY
    )
