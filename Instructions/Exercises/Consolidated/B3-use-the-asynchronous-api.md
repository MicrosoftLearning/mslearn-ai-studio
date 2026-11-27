---
lab:
    title: 'Task 3 – Use the asynchronous API'
    description: 'Rebuild the Wingtip Journeys chat app with the OpenAI SDK asynchronous client, and close the credential cleanly when the app exits.'
    level: 300
    concepts: 'asynchronous API, AsyncOpenAI, async credentials'
    islab: true
    status: 'draft'
---

# Task 3 — Use the asynchronous API

*Part of the **Build a generative AI chat app** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project with a deployed model**, the starter code,
> a `.env` containing `AZURE_OPENAI_ENDPOINT` and `MODEL_DEPLOYMENT`, and an `az login` session.
> Don't have those? Complete [Getting started](B0-getting-started.md) first. This task works in
> **chat-async.py**, which is a separate starter file — nothing from Tasks 1 and 2 needs to be
> finished first.

> **Continuing from a previous task?** If you just finished
> [Task 2](B2-keep-context-and-stream-responses.md), keep your terminal and virtual environment
> open; only the file you're editing changes. It's worth opening **chat-app.py** alongside
> **chat-async.py** so you can see the two versions side by side.

Verify you're ready — from the `python` folder, with your virtual environment active:

```
python ../setup/check_env.py --task 3
```

---

**Goal**: run the same conversation through the SDK's asynchronous client.

**Concept reinforced**: the OpenAI SDK offers an asynchronous option that can increase the
responsiveness of applications when using long-running model or agent operations — and async
credentials must be closed explicitly.

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
<summary>A console app has one user. Why go async at all?</summary>
<div class="concept-body" markdown="1">

Because this console app is a stand-in for a web service. A single model call can take many
seconds, and a synchronous handler blocks its worker for the whole time — so a handful of
concurrent travelers is enough to exhaust the pool.

The async client releases the thread while it waits, which is what lets one process serve many
conversations at once. It's also what you'll need the moment you add a second call per turn,
such as a tool lookup running alongside the model.

</div>
</details>

## Write the asynchronous chat app

1. In the **Explorer** pane, in the `labfiles/B-build-a-generative-ai-chat-app/python` folder, select the **chat-async.py** file (<u>not</u> *chat-app.py*) to open it.
1. Review the existing code. You will add code to use the OpenAI SDK async API to access your model.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces for async** and add the following code to import the namespaces you will need:

    ```python
   # Import namespaces for async
   import asyncio
   from openai import AsyncOpenAI
   from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
    ```

    Note that the credential classes come from `azure.identity.aio` — the asynchronous variants of the ones you'd use in a synchronous app.

1. In the **main** function, note that code to load the endpoint and deployment name from the configuration file has already been provided. Then find the comment **Initialize an async OpenAI client**, and add the following code to create a client for the OpenAI API:

    ```python
   # Initialize an async OpenAI client
   credential = DefaultAzureCredential()
   token_provider = get_bearer_token_provider(
    credential, "https://ai.azure.com/.default"
   )

   async_client = AsyncOpenAI(
        base_url=azure_openai_endpoint,
        api_key=token_provider
   )
    ```

    Keeping a reference to `credential` matters — you'll close it at the end of the function.
    The starter file already declares `credential = None` above the `try` block, so the
    `finally` block can always see it even if something fails before this line runs.

1. In the **main** function, note that code to request a user prompt until the user quits the app has been provided, along with the `last_response_id` tracking you saw in Task 2. Within this loop, find the **Await an asynchronous response** comment, and add the following code:

    ```python
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
    ```

    This code awaits an asynchronous response from the model.

1. At the end of the **main** function, in the **finally** block, find the comment **Close the async client session**. Replace the `pass` statement with the following code to close the asynchronous credential:

    ```python
   # Close the async client session
   if credential is not None:
        await credential.close()
    ```

    Async credentials hold network resources, so closing them avoids warnings about unclosed sessions on exit.

1. Save the changes to the code file. Then, in the terminal pane, use the following command to run the program:

    ```powershell
   python chat-async.py
    ```

    The program should run in the terminal (if not, resolve any errors and try again).

1. When prompted, enter the following prompt:

    ```input
    What's the best time of year to visit Dubai?
    ```

    After a few moments, the app should respond with information about Dubai's seasons.

1. Try a follow-up to confirm context is still being maintained:

    ```input
    And what should I pack?
    ```

1. Enter the prompt `quit` to end the application.

> ✅ **Checkpoint**: The same conversation now runs through the asynchronous client, and the
> app shuts down without leaking an open credential session.

**Stretch**: add streaming to the async version. The event loop is the same as Task 2, but
you'll need `async for` instead of `for`.

---

**Next (optional):** [Task 4 — Ground your app with file search and web search](B4-ground-your-app-with-tools.md)
