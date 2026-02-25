import os
from dotenv import load_dotenv

# Add references

def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the project client

        # Get an OpenAI client from the project

        # Upload file and create vector store

        # Track conversation state
        previous_response_id = None

        while True:
            input_text = input('\nEnter a question (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a question.")
                continue

            # Get a response

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
