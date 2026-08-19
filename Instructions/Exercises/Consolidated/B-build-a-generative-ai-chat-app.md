---
lab:
    title: 'Build a generative AI chat app'
    description: 'Build the Wingtip Journeys travel assistant in code: chat with a model using the OpenAI SDK and Responses API, keep conversation context, stream responses, go asynchronous, and ground it in your own destination guides. A modular lab you can complete end to end or one task at a time.'
    level: 300
    concepts: 'OpenAI SDK, Responses API, streaming, async, file search, web search'
    duration: 35
    islab: true
    status: 'draft'
---

<!--
CONSOLIDATION NOTE (remove before publishing):
"Lab B" consolidates the source exercises 03 (Create a generative AI chat app) and
04a (Create a generative AI app that uses tools) into one modular lab with a Core +
Optional task flow.

Starter code lives in a single folder - labfiles/B-build-a-generative-ai-chat-app/python/ -
shared by every task (one virtual environment, one .env). The completed reference code is in
labfiles/B-build-a-generative-ai-chat-app/Solution/python/.

This landing page is the lab overview. Setup lives in B0-getting-started.md and each task is
its own page (B1-B4) so it can be completed on its own.
-->

# Build a generative AI chat app

**Difficulty** ▰▰▰▱▱ **L300**  (filled bars out of 5; **L100** beginner → **L500** expert)

A model in a playground is a demo. A model behind your own code, holding a conversation and
answering from your company's data, is a product. In this lab you'll make that jump.

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
<summary>Chat Completions or Responses — which API should I use?</summary>
<div class="concept-body" markdown="1">

The **Chat Completions** API is the well-established approach: you assemble a JSON array of
`messages` (a system prompt, then the conversation) and send the whole thing every turn.

The **Responses** API is the newer, unified interface that is increasingly superseding it. The
system prompt becomes `instructions`, the user's turn becomes `input`, and — crucially — the
service can hold conversation state for you, so you chain turns with a response ID instead of
resending the transcript. It's also where tools like file search and web search live.

You'll write both in Task 1, in that order, so the difference is something you've felt rather
than been told.

</div>
</details>

**Your scenario:** you're the AI developer at **Wingtip Journeys**, a travel company that
plans small-group trips. You're building the client application behind the Wingtip Journeys
travel assistant — first as a plain console chat, then as a grounded assistant that answers
from Wingtip Journeys' own destination guides and can look up current information on the web.

You'll start with the **Core** tasks that get you to a working, context-aware chat app as
quickly as possible. From there, a set of **Optional** tasks lets you go deeper.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** tasks of this exercise, you'll be able to:

- **Connect to a deployed model from code** with the OpenAI SDK and Microsoft Entra ID
  authentication, and chat with it using both the **Chat Completions** and **Responses** APIs.
- **Maintain conversational context** across turns and **stream** responses so long answers
  appear as they're generated.

The **Optional** tasks let you additionally:

- Use the SDK's **asynchronous** API for more responsive long-running calls.
- **Ground your app in your own data** with the `file_search` tool over a vector store, and
  reach current information with the `web_search` tool.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** —
so you can pick a single task and do just that one. Every task shares one starter folder, one
virtual environment, and one `.env`, so if you'd rather work straight through, you can.

1. **Start with [Getting started](B0-getting-started.md)** — create your Microsoft Foundry
   project, deploy a model, get the starter code, and set up your `.env`. Every task begins
   here; if you're doing the whole lab in one sitting, you only need to do this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** tasks first (about **35 minutes**) — they end with a responsive,
context-aware chat app. Then expand any **Optional** tasks that interest you. The full lab,
including all optional tasks, takes about **1 hour 15 minutes**.

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Chat with a model from code](B1-chat-with-a-model-from-code.md) | ▰▰▰▱▱ L300 | ~20 min |
| **Core** | [Task 2 – Keep context and stream responses](B2-keep-context-and-stream-responses.md) | ▰▰▰▱▱ L300 | ~15 min |
| *Optional* | [Task 3 – Use the asynchronous API](B3-use-the-asynchronous-api.md) | ▰▰▰▱▱ L300 | ~10 min |
| *Optional* | [Task 4 – Ground your app with file search and web search](B4-ground-your-app-with-tools.md) | ▰▰▰▱▱ L300 | ~30 min |

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~35 min):** do Tasks 1–2.
- **Core + recommended (~1h 5m):** also do **Task 4**, which is where the assistant stops
  guessing and starts answering from Wingtip Journeys' own content.
- **Everything (~1h 15m):** add **Task 3**.

> **One assistant, growing capabilities**: every task runs as a console chat app you start with
> `python <file>.py` and leave with `quit`. Tasks 1–3 build up `chat-app.py` and `chat-async.py`;
> Task 4 applies the same patterns in `tools-app.py` and adds grounding.

## Where this lab starts

This lab assumes you already have a Foundry project with a deployed model. If you'd like to
understand *why* you'd choose that model — and how to measure and safeguard it — the companion
lab **[Choose, evaluate, and safeguard a model](A-choose-evaluate-and-safeguard-a-model.md)**
covers exactly that, entirely in the portal.

## Summary

Across this lab you:

- Used the **OpenAI SDK** with **Microsoft Entra ID** authentication to chat with a model
  deployed in a Microsoft Foundry project, via both the **Chat Completions** and **Responses**
  APIs.
- Maintained **conversational context** with `previous_response_id` and implemented
  **streaming** to deliver a responsive chat experience.
- (Optionally) used the **asynchronous** API, and grounded the assistant in Wingtip Journeys'
  own destination guides with **`file_search`** while reaching live information with
  **`web_search`**.

Together these are the building blocks of every generative AI application: connect, converse,
respond quickly, and answer from data you control.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> Task 4 creates a **vector store** in your project each time it runs. Deleting the resource
> group removes those along with everything else.
