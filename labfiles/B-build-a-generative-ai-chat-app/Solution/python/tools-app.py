import os
from dotenv import load_dotenv
import glob

# Import namespaces
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # Initialize the OpenAI client
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        openai_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )

        # Create vector store and upload files
        print("Creating vector store and uploading files...")
        vector_store = openai_client.vector_stores.create(
            name="wingtip-destination-guides"
        )
        file_streams = [open(f, "rb") for f in glob.glob("guides/*.md")]
        if not file_streams:
            print("No guide files found in the guides folder!")
            return
        file_batch = openai_client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )
        for f in file_streams:
            f.close()
        print(f"Vector store created with {file_batch.file_counts.completed} files.")

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
            response = openai_client.responses.create(
                model=model_deployment,
                instructions="""
                You are a travel assistant that provides information on travel services available from Wingtip Journeys.
                Answer questions about trips offered by Wingtip Journeys using the provided destination guides.
                Search the web for general information about destinations or current travel advice.
                """,
                input=input_text,
                previous_response_id=last_response_id,
                tools=[
                    {
                        "type": "file_search",
                        "vector_store_ids": [vector_store.id]
                    },
                    {
                        "type": "web_search"
                    }
                ]
            )
            print(response.output_text)
            last_response_id = response.id

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
