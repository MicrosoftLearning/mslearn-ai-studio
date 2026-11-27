import os
from dotenv import load_dotenv

# Import namespaces for async
# TODO: import asyncio, AsyncOpenAI, and the async Azure Identity helpers


async def main():

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Declared here so the finally block below can always see it
    credential = None

    try:
        # Get configuration settings
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize an async OpenAI client
        # TODO: create an async token provider and an AsyncOpenAI client


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
            # TODO: await the model response, print it, and remember the response id


    except Exception as ex:
        print(ex)

    finally:
        # Close the async client session
        # TODO: close the credential you created above
        pass


if __name__ == '__main__':
    asyncio.run(main())
