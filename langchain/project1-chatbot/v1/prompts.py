from langchain_core.prompts import ChatPromptTemplate

technical_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a technical assistant specialist in programming languages and software development."),
    ("human","{question}")
])