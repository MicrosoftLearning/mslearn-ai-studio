import os
from dotenv import load_dotenv
import glob

# Import namespaces
# TODO: import OpenAI, and the Azure Identity helpers used for Entra ID authentication


def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the OpenAI client
        # TODO: create a token provider and an OpenAI client for the Wingtip Journeys model


        # Create vector store and upload files
        # TODO: create a vector store and upload the destination guides in guides/


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

            # Get a response using tools
            # TODO: send the prompt with the file_search and web_search tools enabled


    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
