import os
from urllib.request import urlopen, Request
import base64

# Add references


def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_connection = os.getenv("PROJECT_CONNECTION")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")
        
        # Initialize the project client

        

        ## Get a chat client
        

        system_message = "You are an AI assistent in a grocery store that sells fruit."
         

        # Loop until the user types 'quit'
        while True:
            input_text = input("Choose a prompt type (or type 'quit' to exit):\n-1: Text\n-2: Image\n-3: Audio\n")
            if input_text.lower() == "quit":
                break
            elif input_text == "1":
                prompt = input("Enter the prompt: ")
                if len(prompt) == 0:
                    print("Please enter a prompt.")
                else:
                    print("Getting a response to your prompt...")

                    # Get a response to text input
                    

            elif input_text == "2":
                prompt = input("Enter the prompt to accompany the image: ")
                if len(prompt) == 0:
                    print("Please enter a prompt.")
                else:
                    print("Getting a response to your prompt...")

                    # Get a response to image input
                    

            elif input_text == "3":
                prompt = input("Enter the prompt to accompany an audio recording of 'Me gustaría comprar 2 manzanas.': ")
                if len(prompt) == 0:
                    print("Please enter a prompt.")
                else:
                    print("Getting a response to your prompt...")

                    # Get a response to audio input
                    

            else:
                print("Please enter a valid value")
                continue


    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()