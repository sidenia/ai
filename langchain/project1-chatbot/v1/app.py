from llm import get_llm
from prompts import technical_prompt

def main():
    llm = get_llm()
    chain = technical_prompt | llm
    
    print("Welcome to the Technical Support Chatbot! Type 'exit' to quit.")
    while True:
        question = input("You: ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        
        answer = chain.invoke({"question": question})
        response = answer.content if hasattr(answer, 'content') else str(answer)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
