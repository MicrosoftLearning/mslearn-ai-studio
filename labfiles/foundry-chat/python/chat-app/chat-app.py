import os
from dotenv import load_dotenv
# import namespaces
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
# import namespaces

def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # load environment variables from .env file
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        # initialize the OpenAI client with Azure credentials
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
            )

        openai_client = OpenAI(
            base_url=azure_openai_endpoint,
            api_key=token_provider
        )

        # Track responses
        last_response_id = None

        #loop until user wants to exit
        while True:
            input_text = input('\nEnter a prompt (or type "exit" to quit): ')
            if input_text.lower() == "exit":
                break
            if len(input_text.strip()) == 0:
                print("Please enter a valid prompt.")
                continue

            # Get Response
            stream = openai_client.responses.create(
                model=model_deployment,
                instructions="You are a helpful AI assistant that answers questions and provides information.",
                input=input_text,
                previous_response_id=last_response_id,
                stream=True
            )

            for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="", flush=True)
                elif event.type == "response.completed":
                    last_response_id = event.response.id
                    print("\nResponse completed.")
                elif event.type == "response.error":
                    print(f"\nError: {event.error.message}")
                    break

                print()

            # Get a response from the OpenAI API
            # response = openai_client.responses.create(
            #     model=model_deployment,
            #     instructions="You are a helpful AI assistant that answers questions and provides information.",
            #     input=input_text,
            #     previous_response_id=last_response_id,
            # )
            # print(response.output_text)
            # last_response_id = response.id
      

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
