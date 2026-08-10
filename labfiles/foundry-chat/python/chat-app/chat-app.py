import os
import subprocess
from dotenv import load_dotenv

# import namespaces



def main():

    # Clear the console
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

    try:
        # Get configuration settings
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the OpenAI client


        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Get a response


    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()