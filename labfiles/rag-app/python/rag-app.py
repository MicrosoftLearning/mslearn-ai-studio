"""
Required Libraries
pip install python-dotenv azure-ai-projects azure-identity openai
"""

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
import openai

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    try: 
        
        # Get configuration settings 
        load_dotenv()
        project_connection = os.getenv("PROJECT_CONNECTION")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")
        index_name = os.getenv("INDEX_NAME")
        
        # Initialize the project client
        projectClient = AIProjectClient.from_connection_string(
            conn_str=project_connection,
            credential=DefaultAzureCredential())

        # Use the AI search service connection to get service details
        searchConnection = projectClient.connections.get_default(
            connection_type=ConnectionType.AZURE_AI_SEARCH,
            include_credentials=True,
        )
        search_url = searchConnection.endpoint_url
        search_key = searchConnection.key

        ## Get an OpenAI chat client
        aoai_client = projectClient.inference.get_azure_openai_client(api_version="2024-10-21")

        # Loop until the user types 'quit'
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue
            
            # Get a chat completion
            completion = aoai_client.chat.completions.create(
                model=model_deployment,
                messages=[
                    {"role": "system", "content": "You are an AI travel assistant that helps people plan trips."},
                    {"role": "user", "content": input_text},
                ],
                ## additional parameters to apply RAG pattern using the AI Search index
                extra_body={
                    "data_sources":[
                        {
                            "type": "azure_search",
                            "parameters": {
                                "endpoint": search_url,
                                "index_name": index_name,
                                "authentication": {
                                    "type": "api_key",
                                    "key": search_key,
                                }
                            }
                        }
                    ],
                }
            )

            print(completion.choices[0].message.content)


    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()