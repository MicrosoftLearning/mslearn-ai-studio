Video generation with Sora (preview)
Choose your preferred usage method
Sora is an AI model from OpenAI that creates realistic and imaginative video scenes from text instructions and/or input images or video. The model can generate a wide range of video content, including realistic scenes, animations, and special effects. It supports several video resolutions and durations.

Capabilities
Modalities: text → video, image → video, video (generated) → video

Audio: Sora 2 supports audio generation in output videos (similar to the Sora app).

Remix: Sora 2 introduces the ability to remix existing videos by making targeted adjustments instead of regenerating from scratch.

Responsible AI and video generation: Azure OpenAI's video generation models include built-in Responsible AI (RAI) protections to help ensure safe and compliant use. Sora 2 blocks all IP and photorealistic content.

In addition, Azure provides input and output moderation across all image generation models, along with Azure-specific safeguards such as content filtering and abuse monitoring. These systems help detect and prevent the generation or misuse of harmful, unsafe, or policy-violating content.

Customers can learn more about these safeguards and how to customize them on the Content filtering page.

Model comparison
Azure OpenAI supports two versions of Sora:

Sora (or Sora 1): Azure OpenAI–specific implementation released as an API in early preview.
Sora 2: The latest OpenAI-based API, now available with the Azure OpenAI v1 API.
Aspect	Sora 1 (Azure OpenAI)	Sora 2 (OpenAI-based API)
Model type	Azure-specific API implementation	Adapts OpenAI’s latest Sora API using v1 API
Availability	Available exclusively on Azure OpenAI (Preview)	Rolling out on Azure; Sora 2 Pro coming later
Modalities supported	text → video, image → video, video → video	text → video, image → video, video (generated) → video
Audio generation	❌ Not supported	✅ Supported in outputs
Remix capability	❌ Not supported	✅ Supported — make targeted edits to existing videos
API behavior	Uses Azure-specific API schema	Aligns with OpenAI’s native Sora 2 schema
Performance & fidelity	Early preview; limited realism and motion range	Enhanced realism, physics, and temporal consistency
Intended use	Enterprise preview deployments	Broader developer availability with improved API parity
Billing	Billed differently across duration and resolutions	Per second billing information
Quickstart
Generate video clips using the Azure OpenAI service. Video generation is an asynchronous process. You create a job request with your text prompt and video format specifications, and the model processes the request in the background. You check the status of the video generation job and, once it finishes, retrieve the generated video through a download URL. The example uses the Sora model.

Prerequisites
An Azure subscription. Create one for free.
An Azure OpenAI resource created in a supported region. See Region availability. For more information, see Create a resource and deploy a model with Azure OpenAI.
Go to Microsoft Foundry portal
Browse to the Foundry portal and sign in with the credentials associated with your Azure OpenAI resource. During or after the sign-in workflow, select the appropriate directory, Azure subscription, and Azure OpenAI resource.

From the Foundry landing page, create or select a new project. Navigate to the Models + endpoints page on the left nav. Select Deploy model and then choose the Sora video generation model from the list. Complete the deployment process.

On the model's page, select Open in playground.

Try out video generation
Start exploring Sora video generation with a no-code approach through the Video playground. Enter your prompt into the text box and select Generate. Video generation typically takes 1 to 5 minutes depending on your settings. When the AI-generated video is ready, it appears on the page.

 Note

The content generation APIs come with a content moderation filter. If Azure OpenAI recognizes your prompt as harmful content, it doesn't return a generated video. For more information, see Content filtering.

In the Video playground, you can also view Python and cURL code samples, which are prefilled according to your settings. Select the code button at the top of your video playback pane. You can use this code to write an application that completes the same task.

Clean up resources
If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

Azure portal
Azure CLI
Responsible AI and video generation
Azure OpenAI's image generation models include built-in Responsible AI (RAI) protections to help ensure safe and compliant use.

In addition, Azure provides input and output moderation across all image generation models, along with Azure-specific safeguards such as content filtering and abuse monitoring. These systems help detect and prevent the generation or misuse of harmful, unsafe, or policy-violating content.

Currently the Sora 2 API enforces several content restrictions:

Only content suitable for audiences under 18 (a setting to bypass this restriction will be available in the future).
Copyrighted characters and copyrighted music will be rejected.
Real people—including public figures—cannot be generated.
Input images with faces of humans are currently rejected.
Make sure prompts, reference images, and transcripts respect these rules to avoid failed generations.

Sora 2 API reference
The Sora 2 API provides 5 endpoints, each with distinct capabilities.

Create Video: Start a new render job from a prompt, with optional reference inputs or a remix ID.
Get Video Status: Retrieve the current state of a render job and monitor its progress
Download Video: Fetch the finished MP4 once the job is completed.
List Videos: Enumerate your videos with pagination for history, dashboards, or housekeeping.
Delete Videos: Delete an individual video ID from Azure OpenAI’s storage
API parameters
Parameter	Type	Sora 2
Prompt	String (required)	Natural-language description of the shot. Include shot type, subject, action, setting, lighting, and any desired camera motion to reduce ambiguity. Keep it single-purpose for best adherence.
Model	String (optional)	Sora-2 (default)
Size (Output resolution in width × height)	String (optional)	Portrait: 720×1280
Landscape: 1280×720
Default: 720×1280
Seconds	String (optional)	4 / 8 / 12
Default: 4
Input reference	File (optional)	Single reference image used as a visual anchor for the first frame.
Accepted MIME types: image/jpeg, image/png, image/webp. Must match size exactly.
Remix_video_id	String (optional)	ID of a previously completed video (e.g., video_...) to reuse structure, motion, and framing. Same as Sora 2
Sora 2 API uses the v1 API and has the same structure as the OpenAI API.

videos.create()
You'll need to update to the latest version of the OpenAI client with pip install openai --upgrade to prevent AttributeError: 'OpenAI' object has no attribute 'videos'.

Microsoft Entra ID
API Key
Environment Variables
Response
Python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

video = client.videos.create(
    model="sora-2", # Replace with Sora 2 model deployment name
    prompt="A video of a cool cat on a motorcycle in the night",
)

print("Video generation started:", video)
Create a video and poll job status
Call GET /videos/{video_id} with the ID returned from the create call. The response shows the job’s current status, progress percentage, and any errors.

Expected states are queued, in_progress, completed, and failed.

Microsoft Entra ID
API Key
Environment Variables
Response
Synchronous:

Use this version if testing in Jupyter Notebooks to avoid RuntimeError: asyncio.run() cannot be called from a running event loop

Python
import time
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
    base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
    api_key=token_provider,
)

# Create the video (don't use create_and_poll)
video = client.videos.create(
    model="sora-2", # Replace with Sora 2 model deployment name
    prompt="A video of a cat on a motorcycle",
)

print(f"Video creation started. ID: {video.id}")
print(f"Initial status: {video.status}")

# Poll every 20 seconds
while video.status not in ["completed", "failed", "cancelled"]:
    print(f"Status: {video.status}. Waiting 20 seconds...")
    time.sleep(20)
    
    # Retrieve the latest status
    video = client.videos.retrieve(video.id)

# Final status
if video.status == "completed":
    print("Video successfully completed!")
    print(video)
else:
    print(f"Video creation ended with status: {video.status}")
    print(video)
Async:

Python
import asyncio
from openai import AsyncOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AsyncOpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

async def main() -> None:
    video = await client.videos.create_and_poll(
        model="sora-2", # Replace with Sora 2 model deployment name
        prompt="A video of a cat on a motorcycle",
    )

    if video.status == "completed":
        print("Video successfully completed: ", video)
    else:
        print("Video creation failed. Status: ", video.status)

asyncio.run(main())
Download video
Microsoft Entra ID
API Key
Environment Variables
Response
Python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

video_id = "your_video_id_here"

content = client.videos.download_content(video_id, variant="video")
content.write_to_file("video.mp4")

print("Saved video.mp4")
Video generation from reference source
The input_reference parameter allows you to transform existing images using Sora 2. The resolution of the source image and final video must match. Supported values are 720x1280, and 1280x720.

Microsoft Entra ID
API Key
Environment Variables
Response
Local reference file:

Python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

# With local file
video = client.videos.create(
    model="sora-2",
    prompt="Describe your desired output within the context of the reference image/video",
    size="1280x720",
    seconds=8,
    input_reference=open("test.png", "rb"), # This assumes the image test.png is in the same directory as the executing code
)

print("Video generation started:", video)

URL based reference file:

Python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import requests
from io import BytesIO

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

# With image URL
image_url = "https://path-to-your-file/image_file_name.jpg"
response = requests.get(image_url)
image_data = BytesIO(response.content)
image_data.name = "image_file_name.jpg"

video = client.videos.create(
    model="sora-2",
    prompt="Describe your desired output within the context of the reference image/video",
    size="1280x720",
    seconds=8,
    input_reference=image_data,
)

print("Video generation started:", video)
Remix video
The remix feature allows you to modify specific aspects of an existing video while preserving its core elements. By referencing the previous video id from a successfully completed generation, and supplying an updated prompt the system maintains the original video's framework, scene transitions, and visual layout while implementing your requested changes. For optimal results, limit your modifications to one clearly articulated adjustment—narrow, precise edits retain greater fidelity to the source material and minimize the likelihood of generating visual defects.

Microsoft Entra ID
API Key
Environment Variables
Response
Python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

video = client.videos.remix(
    video_id="<previous_video_id>",
    prompt="Shift the color palette to teal, sand, and rust, with a warm backlight."
)

print("Video generation started:", video)