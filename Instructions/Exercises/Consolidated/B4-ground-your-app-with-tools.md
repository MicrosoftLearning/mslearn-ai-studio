---
lab:
    title: 'Task 4 – Ground your app with file search and web search'
    description: 'Extend the Wingtip Journeys assistant with tools: upload destination guides to a vector store for file_search, and add web_search so it can answer with current information.'
    level: 300
    concepts: 'tools, vector stores, file_search, web_search, grounding'
    islab: true
    status: 'draft'
---

# Task 4 — Ground your app with file search and web search

*Part of the **Build a generative AI chat app** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project with a deployed model**, the starter code
> (including the `guides/` folder), a `.env` containing `AZURE_OPENAI_ENDPOINT` and
> `MODEL_DEPLOYMENT`, and an `az login` session. Don't have those? Complete
> [Getting started](B0-getting-started.md) first. This task works in **tools-app.py**, a
> separate starter file — nothing from Tasks 1–3 needs to be finished first, though the client
> setup will look familiar if you did Task 1.

> **Continuing from a previous task?** If you just finished
> [Task 3](B3-use-the-asynchronous-api.md), keep your terminal and virtual environment open.
> This task goes back to the synchronous client, so copy the imports and client setup from
> **chat-app.py** rather than **chat-async.py**.

Verify you're ready — from the `python` folder, with your virtual environment active:

```
python ../setup/check_env.py --task 4
```

---

**Goal**: stop the assistant guessing. By the end of this task it answers Wingtip Journeys
questions from Wingtip Journeys' own content, and everything else from the live web.

**Concept reinforced**: extending a model with **tools** — `file_search` over a vector store you
populate, and `web_search` for current information the model was never trained on.

## See the problem first, in the playground

Before writing code, let's see why grounding data matters.

1. In the Foundry portal, open your model deployment in the model playground.
1. In the **Instructions** field, enter the following prompt:

    ```
   You are a travel assistant that provides information on travel services available from Wingtip Journeys.
    ```

1. In the chat pane, enter the query `What are some recommended tourist activities in New York next month?` and review the response.

    The response should be fairly generic — the model provides general knowledge based on its training data, but doesn't have access to current information about what's happening in New York next month.

1. In the pane on the left, under the instructions, in the **Tools** section, select **Add** and add the **web_search** tool.

1. In the chat pane, enter the same query `What are some recommended tourist activities in New York next month?` and review the response.

    This time, the model uses the *web_search* tool to find current information about activities in New York.

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
<summary>Two tools, two different jobs</summary>
<div class="concept-body" markdown="1">

`web_search` fixes a **recency** problem: the model's training data has a cutoff, and "what's on
in New York next month" is on the wrong side of it.

`file_search` fixes a **privacy and authority** problem: no public model has ever seen Wingtip
Journeys' partner hotel list or cancellation terms, and you wouldn't want it to invent them.
You upload that content to a **vector store**, and the tool retrieves the relevant passages at
query time.

Give the model both, describe when to use each in the instructions, and it routes each question
to the right source.

</div>
</details>

## Write code to implement chat with tools

1. In the **Explorer** pane, in the `labfiles/B-build-a-generative-ai-chat-app/python` folder, select the **tools-app.py** file to open it.
1. Review the existing code. You will add code to use the OpenAI SDK to access your model. Note the **guides** folder alongside it — five Markdown files describing Wingtip Journeys trips, which you're about to make searchable.

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

1. In the **main** function, find the comment **Create vector store and upload files**, and add the following code:

    ```python
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
    ```

    This code creates a vector store for your model, and uploads the destination guides to it. We'll use this vector store with the *file_search* tool.

1. In the **main** function, note that code to request a user prompt until the user quits the app has been provided. Within this loop, find the **Get a response using tools** comment.

    > **Try it first**: before reading on, predict the shape. You already know how to call
    > `responses.create` from Task 1. What extra parameter carries the tools, and how would the
    > `file_search` tool know *which* vector store to search?

<details markdown="1">
<summary>Show a solution</summary>

Add the following code under the **Get a response using tools** comment:

```python
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
```

This code submits a prompt and specifies that the *file_search* tool can be used to search the vector store, and the *web_search* tool can be used for general web searches. Note that the instructions tell the model *when* to prefer each one.

</details>

1. Save the changes to the code file. If you haven't already signed in to Azure in this terminal, do so now:

    ```powershell
    az login
    ```

1. After you have signed in, enter the following command to run the application:

    ```powershell
   python tools-app.py
    ```

    The app creates the vector store and uploads the guides before the first prompt appears. The program should then run in the terminal (if not, resolve any errors and try again).

1. When prompted, enter `What's happening in San Francisco next month?` and review the response from your generative AI model.

    The response should include information retrieved using the *web_search* tool.

1. Try this follow-up question: `Which hotels does Wingtip Journeys use there?`

    The response should include information retrieved using the *file_search* tool — specifically, the two partner properties named in the San Francisco guide.

1. Try one more, to see the model choose between its two sources:

    ```
    Do I need travel insurance for the London trip, and what's the weather like there in May?
    ```

    The insurance answer should come from the Wingtip Journeys guides; the weather answer should come from the web.

1. When you're finished, enter `quit` to exit the program.

> ✅ **Checkpoint**: The Wingtip Journeys assistant answers company questions from company
> content and current questions from the live web — and it decides which is which.

**Stretch**: add a sixth guide of your own to the `guides/` folder, re-run the app, and ask a
question only that file can answer.

---

**Next:** You've completed the optional tasks. Head back to the
[lab overview](B-build-a-generative-ai-chat-app.md) for a summary and clean-up steps.
