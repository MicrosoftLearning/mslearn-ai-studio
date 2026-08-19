import os
from dotenv import load_dotenv

# Import namespaces for async
import asyncio
from openai import AsyncOpenAI
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider


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
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(
            credential, "https://ai.azure.com/.default"
        )

        async_client = AsyncOpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )

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
            response = await async_client.responses.create(
                model=model_deployment,
                instructions="You are the Wingtip Journeys travel assistant. You answer traveler questions and provide practical trip-planning information.",
                input=input_text,
                previous_response_id=last_response_id
            )
            assistant_text = response.output_text
            print("Assistant:", assistant_text)
            last_response_id = response.id

    except Exception as ex:
        print(ex)

    finally:
        # Close the async client session
        if credential is not None:
            await credential.close()


if __name__ == '__main__':
    asyncio.run(main())
