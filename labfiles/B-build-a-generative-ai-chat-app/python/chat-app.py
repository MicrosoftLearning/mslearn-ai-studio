import os
from dotenv import load_dotenv

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


        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Get a response
            # TODO: send the prompt to the model and print the reply


    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
