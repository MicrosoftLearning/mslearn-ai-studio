import os
import subprocess
from dotenv import load_dotenv

# import namespaces for async



async def main():

    # Clear the console
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

    try:
        # Get configuration settings
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize an async OpenAI client


        # Track responses
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Await an asynchronous response


    except Exception as ex:
        print(ex)

    finally:
        # Close the async client session



if __name__ == '__main__':
    asyncio.run(main())