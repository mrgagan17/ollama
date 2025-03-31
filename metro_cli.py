from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import sys

def initialize_ollama():
    try:
        # Test connection to Ollama
        llm = Ollama(model="llama3")
        llm("test")  # Simple test query
        return llm
    except Exception as e:
        print(f"Failed to connect to Ollama: {str(e)}")
        print("\nPlease make sure Ollama is running:")
        print("1. Download Ollama from https://ollama.com")
        print("2. Run these commands in your terminal:")
        print("   ollama pull llama3")
        print("   ollama serve")
        print("3. Then restart this program")
        sys.exit(1)

template = """
Answer the question concisely based on the conversation history.

Conversation History:
{context}

Question: {question}

Answer: 
"""

def main():
    # Initialize Ollama with connection check
    llm = initialize_ollama()
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    context = ""
    print("Welcome to the AI ChatBot! Type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            if not user_input:
                print("Bot: Please enter a question.")
                continue

            # Invoke the chain with error handling
            result = chain.invoke({
                "context": context, 
                "question": user_input
            })
            
            print(f"\nBot: {result}")
            context += f"\nUser: {user_input}\nAI: {result}"

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nBot: Error processing your request: {str(e)}")

if __name__ == "__main__":
    main()