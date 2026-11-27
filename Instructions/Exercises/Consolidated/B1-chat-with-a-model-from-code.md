---
lab:
    title: 'Task 1 – Chat with a model from code'
    description: 'Connect to a deployed model with the OpenAI SDK and Entra ID authentication, then chat with it using the Chat Completions API and the newer Responses API.'
    level: 300
    concepts: 'OpenAI SDK, Entra ID authentication, Chat Completions API, Responses API'
    islab: true
    status: 'draft'
---

# Task 1 — Chat with a model from code

*Part of the **Build a generative AI chat app** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project with a deployed model**, the starter code,
> and a `.env` containing `AZURE_OPENAI_ENDPOINT` and `MODEL_DEPLOYMENT`. Don't have those yet?
> Complete [Getting started](B0-getting-started.md) first. You also need to be signed in with
> `az login` in the terminal you'll run from.

Verify you're ready — from the `python` folder, with your virtual environment active:

```
python ../setup/check_env.py --task 1
```

---

**Goal**: get the Wingtip Journeys assistant talking to a real model from a Python console app.

**Concept reinforced**: connecting to a Foundry model deployment with the OpenAI SDK and
Microsoft Entra ID authentication, then comparing the two request styles the SDK offers.

You'll write both APIs in this task: the well-established **Chat Completions** API first, then
the newer **Responses** API that supersedes it. Writing them back to back is the fastest way to
see what the newer API actually simplifies.

<style>
/* "Ask Wren" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
  font-size:.85em; font-weight:600; color:#0f6cbd; background:#0f6cbd12;
  border:1px solid #0f6cbd33; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Wren: "; font-weight:700; }
details.concept > summary:hover { background:#0f6cbd; color:#fff; border-color:#0f6cbd; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #0f6cbd33; border-top:none;
  border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#0f6cbd08; font-size:.95em; }
</style>

<details markdown="1" class="concept">
<summary>Why a token provider instead of an API key?</summary>
<div class="concept-body" markdown="1">

`DefaultAzureCredential` picks up whatever identity is already available — your `az login`
session locally, a managed identity in Azure — and `get_bearer_token_provider` turns that into
tokens the SDK refreshes automatically.

The practical benefit is that the same line of code works on your laptop and in production,
with no secret in the repo and nothing to rotate. An API key would work here too; it just
isn't something you'd want to ship.

</div>
</details>

## Use the Chat Completions API to chat with the model

1. In the **Explorer** pane, in the `labfiles/B-build-a-generative-ai-chat-app/python` folder, select the **chat-app.py** file (<u>not</u> *chat-async.py*) to open it.
1. Review the existing code. You will add code to use the OpenAI SDK to access your model.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespaces you will need to use the OpenAI SDK:

    ```python
   # Import namespaces
   from openai import OpenAI
   from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

1. In the **main** function, note that code to load the endpoint and deployment name from the configuration file has already been provided. Then find the comment **Initialize the OpenAI client**, and add the following code to create a client for the OpenAI API:

    ```python
   # Initialize the OpenAI client
   token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
   )

   openai_client = OpenAI(
        base_url=azure_openai_endpoint,
        api_key=token_provider
   )
    ```

1. In the **main** function, note that code to request a user prompt until the user quits the app has been provided. Within this loop, find the **Get a response** comment, and add the following code:

    ```python
   # Get a response
   completion = openai_client.chat.completions.create(
        model=model_deployment,
        messages=[
            {
                "role": "system",
                "content": "You are the Wingtip Journeys travel assistant. You answer traveler questions and provide practical trip-planning information."
            },
            {
                "role": "user",
                "content": input_text
            }
        ]
   )
   print(completion.choices[0].message.content)
    ```

    Note that the *ChatCompletions* API uses a JSON collection of *messages* to encapsulate the conversation. Often, these consist of a *system prompt* that provides instructions to the model, and a *user prompt* that includes the user's input.

1. Save the changes to the code file. If you haven't already signed in to Azure in this terminal, do so now:

    ```powershell
    az login
    ```

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. After you have signed in, enter the following command to run the application:

    ```powershell
   python chat-app.py
    ```

    The program should run in the terminal (if not, resolve any errors and try again).

1. When prompted, enter the following prompt:

    ```input
    What should I know before visiting London for the first time?
    ```

    After a few moments, the app should respond with some first-timer advice for London.

1. Enter the prompt `quit` to end the application.

## Use the Responses API to chat with the model

While the *ChatCompletions* API is widely used, it is increasingly being superseded by the
newer *Responses* API. Let's update the code to use it.

> **Try it first**: before reading on, predict what changes. Where does the system prompt go?
> What happens to the `messages` array? How do you read the reply text?

<details markdown="1">
<summary>Show a solution</summary>

1. In the **chat-app.py** code, in the **main** function, replace the code under the comment **Get a response** with the following code that uses the *Responses* API:

    ```python
   # Get a response
   response = openai_client.responses.create(
                model=model_deployment,
                instructions="You are the Wingtip Journeys travel assistant. You answer traveler questions and provide practical trip-planning information.",
                input=input_text
   )
   print(response.output_text)
    ```

    Note the simpler syntax in which the system message is assigned to the *instructions* parameter, and the user prompt is assigned to the *input* parameter.

</details>

1. Save the changes to the code, and in the terminal pane, re-run the application (`python chat-app.py`).
1. When prompted, enter the same prompt as before:

    ```input
    What should I know before visiting London for the first time?
    ```

    After a few moments, the app should once again respond with advice for London.

1. Enter the following prompt to try to continue the conversation:

    ```input
    How does that compare to New York?
    ```

    The app should respond in a way that indicates it doesn't understand what "that" refers to. The conversation context has been lost. Task 2 fixes that.

1. Enter the prompt `quit` to end the application.

> ✅ **Checkpoint**: Your console app authenticates with Entra ID, calls a model deployed in
> your Foundry project, and you've written the same interaction with both the Chat Completions
> and Responses APIs.

**Stretch**: change the `instructions` so the assistant refuses to recommend hotels and
restaurants, in line with the Wingtip Journeys house rules. How reliably does it comply?

---

**Next:** [Task 2 — Keep context and stream responses](B2-keep-context-and-stream-responses.md)
