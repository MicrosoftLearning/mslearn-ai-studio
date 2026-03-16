import os
from dotenv import load_dotenv
import glob

# Import namespaces



def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("API_KEY")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the OpenAI client



        # Create vector store and upload files



        # Track conversation state
        last_response_id = None

        # Loop until the user wants to quit
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
