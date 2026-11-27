---
lab:
    title: 'Task 2 – Keep context and stream responses'
    description: 'Chain turns with previous_response_id so the Wingtip Journeys assistant remembers the conversation, then stream responses so long answers appear as they are generated.'
    level: 300
    concepts: 'conversation state, previous_response_id, streaming responses'
    islab: true
    status: 'draft'
---

# Task 2 — Keep context and stream responses

*Part of the **Build a generative AI chat app** lab. New here? Start with [Getting started](B0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project with a deployed model**, the starter code,
> a `.env` containing `AZURE_OPENAI_ENDPOINT` and `MODEL_DEPLOYMENT`, and an `az login` session.
> Don't have those? Complete [Getting started](B0-getting-started.md) first.
>
> This task edits **chat-app.py**, and assumes it already calls the Responses API. If you're
> starting here, add the imports, the client, and the Responses call from
> [Task 1](B1-chat-with-a-model-from-code.md) first — they're about ten lines and each is shown
> in full on that page.

> **Continuing from a previous task?** If you just finished
> [Task 1](B1-chat-with-a-model-from-code.md), **chat-app.py** is already exactly where this
> task starts. Keep your terminal and virtual environment open and go straight to *Add
> conversation tracking*.

Verify you're ready — from the `python` folder, with your virtual environment active:

```
python ../setup/check_env.py --task 2
```

---

**Goal**: turn a sequence of unrelated questions into an actual conversation, and make long
answers feel fast.

**Concept reinforced**: the Responses API keeps conversation state on the service, so you chain
turns with a response ID instead of resending the transcript — and `stream=True` turns one
response into a sequence of events you can render as they arrive.

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
<summary>Why does passing one ID beat resending the whole conversation?</summary>
<div class="concept-body" markdown="1">

Because the transcript grows, and you pay for it — every turn you resend is input tokens
charged again, and eventually it stops fitting in the context window at all.

Chaining with `previous_response_id` hands that bookkeeping to the service. It also unlocks
something you can't easily do with a local transcript: pass the ID of *any* earlier response to
branch the conversation, redirect it, or resume a thread you abandoned three turns ago.

</div>
</details>

## Add conversation tracking

To maintain the conversational context, we need to include references to previous responses in
each new request.

1. In the **chat-app.py** code, in the **main** function, find the comment **Loop until the user wants to quit**, and add the following code <u>above</u> it (*before* the loop):

    ```python
   # Track responses
   last_response_id = None
    ```

1. Modify the code under the comment **Get a response** with the following code to pass the previous response ID on the request, and then obtain the new response ID so it can be added next time.

    ```python
   # Get a response
   response = openai_client.responses.create(
                model=model_deployment,
                instructions="You are the Wingtip Journeys travel assistant. You answer traveler questions and provide practical trip-planning information.",
                input=input_text,
                previous_response_id=last_response_id,
   )
   print(response.output_text)
   last_response_id = response.id
    ```

    Using this technique, you can pass the ID of the previous response to maintain context. You could also implement more complex logic to pass an ID from any previous response to redirect a conversation or resume a previous conversational thread.

1. Save the changes to the code, and in the terminal pane, re-run the application (`python chat-app.py`).
1. When prompted, enter:

    ```input
    What should I know before visiting London for the first time?
    ```

    After a few moments, the app should respond with advice for London.

1. Enter the following prompt to try to continue the conversation:

    ```input
    How does that compare to New York?
    ```

    This time, the app should respond with a comparison of the two cities. The response may be quite lengthy, and the app waits until it has all been received from the model before displaying it, which may make the app seem unresponsive. We'll fix that next!

1. Enter the prompt `quit` to end the application.

## Implement streaming responses

To handle long responses, you can use *streaming* to start processing partial responses before
the full text has been returned.

> **Try it first**: predict what a streamed response looks like in code. If the reply arrives in
> pieces, what do you loop over — and where does the response ID come from now that there's no
> single response object to read `.id` from?

<details markdown="1">
<summary>Show a solution</summary>

1. In the **chat-app.py** code, in the **main** function, replace the code under the comment **Get a response** with the following code that uses *streaming*:

    ```python
   # Get a response
   stream = openai_client.responses.create(
                model=model_deployment,
                instructions="You are the Wingtip Journeys travel assistant. You answer traveler questions and provide practical trip-planning information.",
                input=input_text,
                previous_response_id=last_response_id,
                stream=True
   )
   for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")
        elif event.type == "response.completed":
            last_response_id = event.response.id
   print()
    ```

    Note that the *stream=True* parameter creates a streamed response in which *events* occur as each new chunk (or *delta*) is ready for processing. The response ID now arrives on the `response.completed` event rather than on a single returned object.

</details>

1. Save the changes to the code, and in the terminal pane, re-run the application (`python chat-app.py`).
1. When prompted, enter the same prompt as before:

    ```input
    What should I know before visiting London for the first time?
    ```

    After a few moments, the app should start responding. The response should appear incrementally as each chunk is returned.

1. Enter the following prompt to try to continue the conversation:

    ```input
    How does that compare to New York?
    ```

    Again, the response should be displayed incrementally — and it should still know what "that" refers to.

1. Enter the prompt `quit` to end the application.

> ✅ **Checkpoint**: The Wingtip Journeys assistant now holds a multi-turn conversation and
> renders answers as they're generated. That's a shippable console experience.

**Stretch**: print the response ID after each turn, then experiment with passing an *earlier*
ID to branch the conversation back to a previous point.

---

**Next (optional):** [Task 3 — Use the asynchronous API](B3-use-the-asynchronous-api.md)
