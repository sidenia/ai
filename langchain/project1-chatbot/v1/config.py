import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # langchain_langgraph/project1-chatbot/v1
AUTH_DIR = os.path.join(BASE_DIR, "..", "..", "..", "auth")

OPENAI_API_KEY = open(os.path.join(AUTH_DIR, "openai_key.txt")).read().strip()