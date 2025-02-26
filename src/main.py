import os
from langchain_services.chain_builder import setup_chatbot
from utils.constants import GREETINGS

# Initialize environment variables
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def main():
    """
    Main function to run the chatbot in command line interface
    
    This function initializes the chatbot and handles the conversation loop
    """
    print("Initializing chatbot...")
    chatbot = setup_chatbot()
    
    print("Chatbot is ready! Type 'quit' to exit.")
    
    while True:
        query = input("\nYou: ").strip()
        if query.lower() == 'quit':
            break
        
        # Handle greetings directly
        if any(greet in query.lower() for greet in GREETINGS):
            print("\nChatbot: Hey! How can I assist you today?")
            continue
            
        try:
            result = chatbot.invoke({"question": query})
            
            # Handle cases where no relevant information is found
            if "help@gmail.com" in result["answer"].lower():
                print("\nChatbot: I don't have information about that. Please contact our Sales Team at help@gmail.com.")
            else:
                print("\nChatbot:", result["answer"])
                
        except Exception as e:
            print(f"\nChatbot: An error occurred. Please try again or contact support. Error: {str(e)}")

if __name__ == "__main__":
    main()