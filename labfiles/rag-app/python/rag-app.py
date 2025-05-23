import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings
        load_dotenv()
        open_ai_endpoint = os.getenv("OPEN_AI_ENDPOINT")
        open_ai_key = os.getenv("OPEN_AI_KEY")
        chat_model = os.getenv("CHAT_MODEL")
        embedding_model = os.getenv("EMBEDDING_MODEL")
        search_url = os.getenv("SEARCH_ENDPOINT")
        search_key = os.getenv("SEARCH_KEY")
        index_name = os.getenv("INDEX_NAME")


        # Get an Azure OpenAI chat client
        chat_client = AzureOpenAI(
            api_version = "2024-12-01-preview",
            azure_endpoint = open_ai_endpoint,
            api_key = open_ai_key
        )


        # Initialize prompt with system message
        prompt = [
            {"role": "system", "content": "You are a travel assistant that provides information on travel services available from Margie's Travel."}
        ]

        # Loop until the user types 'quit'
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Add the user input message to the prompt
            prompt.append({"role": "user", "content": input_text})

            # Additional parameters to apply RAG pattern using the AI Search index
            rag_params = {
                "data_sources": [
                    {
                        # he following params are used to search the index
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": search_url,
                            "index_name": index_name,
                            "authentication": {
                                "type": "api_key",
                                "key": search_key,
                            },
                            # The following params are used to vectorize the query
                            "query_type": "vector",
                            "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": embedding_model,
                            },
                        }
                    }
                ],
            }

            # Submit the prompt with the data source options and display the response
            response = chat_client.chat.completions.create(
                model=chat_model,
                messages=prompt,
                extra_body=rag_params
            )
            completion = response.choices[0].message.content
            print(completion)

            # Add the response to the chat history
            prompt.append({"role": "assistant", "content": completion})

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()