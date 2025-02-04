import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

# Add AI Projects reference


def main(): 
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_connection = os.getenv("PROJECT_CONNECTION")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")
        
        # Initialize the project client
        

        ## Get a chat client
         

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


    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()