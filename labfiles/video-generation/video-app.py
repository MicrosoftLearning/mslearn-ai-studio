import os
from dotenv import load_dotenv

# Add references
# Add references
import time
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Get configuration settings
load_dotenv()
endpoint = os.getenv("OPENAI_BASE_URL")
model_deployment = os.getenv("MODEL_DEPLOYMENT")

# Initialize the OpenAI client with Azure credentials
# Initialize the OpenAI client with Azure credentials
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider(),
)

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try:       
        print("=== Video Generation Application ===\n")
        

        print("Step 1: Generating video from text prompt...")
        # Generate a video from a text prompt

        if video.status == "completed":
            download_video(video.id, "original_video.mp4")
            original_video_id = video.id
            
            # Step 2: Remix the video with a different style
            print("\nStep 2: Remixing the video with a new color palette...")
            remixed = remix_video(
                original_video_id,
                "Shift the color palette to warm sunset tones with golden light"
            )
            
            if remixed.status == "completed":
                download_video(remixed.id, "remixed_video.mp4")

        print("\nStep 3: Generating a video from a reference image...")
        # Generate a video from a reference image
        
        print("\n=== Video generation complete ===")

    except Exception as ex:
        print(ex)


def poll_video_status(video_id):
    """Poll the video status every 20 seconds until it completes or fails."""

    # Poll video status until completion


def remix_video(video_id, prompt):
    """Create a remix of an existing video with a new prompt."""
    print(f"Starting video remix for: {video_id}")
    
    # Remix an existing video
    

def download_video(video_id, output_filename="output.mp4"):
    """Download the completed video to a local file."""
    print(f"Downloading video {video_id}...")

    # Download the completed video


def generate_video_from_image(image_path, prompt, size="1280x720", seconds=8):
    """Generate a video using a reference image as the starting frame."""
    print(f"Starting video generation from image: {image_path}")
    
    # Create the video with an image reference
    

    print(f"Video creation started. ID: {video.id}")
    print(f"Initial status: {video.status}")
    
    # Poll for completion
    video = poll_video_status(video.id)
    return video

if __name__ == '__main__': 
    main()