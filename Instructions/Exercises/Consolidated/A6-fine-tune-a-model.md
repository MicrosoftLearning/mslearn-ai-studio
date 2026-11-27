---
lab:
    title: 'Task 6 – Fine-tune a model for a consistent voice'
    description: 'Fine-tune a model on Wingtip Journeys training data so the travel assistant answers in a consistent house voice, then compare it against the base model.'
    level: 400
    concepts: 'supervised fine-tuning, training data, JSONL, model comparison'
    islab: true
    status: 'draft'
---

# Task 6 — Fine-tune a model for a consistent voice

*Part of the **Choose, evaluate, and safeguard a model** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project in a region that supports fine-tuning** —
> at the time of writing, **North Central US** or **Sweden Central**. This is the one task in
> the lab with a region constraint, so if your project is elsewhere, create a second project
> in one of those regions using [Getting started](A0-getting-started.md). You also need the
> training dataset from this repo (linked below). No local code or `.env` file is required —
> everything happens in the portal.

> **Continuing from a previous task?** Nothing carries over except the project itself. The
> earlier tasks used `gpt-5.2`; this task deploys and tunes **`gpt-4.1`**, because that's the
> model that currently supports supervised fine-tuning with a Developer deployment. Your
> `gpt-5.2` deployment can stay where it is.

> \* **This task takes a long time.** Fine-tuning depends on cloud infrastructure that can take
> a variable amount of time to provision depending on data center capacity and concurrent
> demand. Budget around **90 minutes**, most of it waiting. Start the job first, then use the
> waiting time for the rest of the task (or another task in this lab). If things are taking a
> while, consider reviewing the
> [Microsoft Foundry fine-tuning documentation](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry)
> or taking a break. It is possible some processes may time out or appear to run indefinitely.

---

When you want a language model to behave a certain way, you can use prompt engineering to
define the desired behavior. When you want to improve the *consistency* of that behavior, you
can fine-tune a model — then compare it against your prompt-engineering approach to evaluate
which method best fits your needs.

Wingtip Journeys has a house voice: warm, playful, and always ending with a question that
keeps the traveler dreaming. It also has a hard rule — the assistant inspires, it does not
book. Prompt engineering gets you most of the way there. Fine-tuning is how you make it stick.

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
<summary>Why gpt-4.1 here, when the rest of the lab used gpt-5.2?</summary>
<div class="concept-body" markdown="1">

Not every model supports every customization method. **Supervised fine-tuning** — showing the
model example conversations and letting it learn the pattern — is the method this task
teaches, and it's currently supported on `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o`,
and `gpt-4o-mini`. `gpt-5` supports *reinforcement* fine-tuning instead, and access to it is
gated by invitation.

This is a normal part of the job: the newest model isn't automatically the right one for a
given technique. Always check the
[supported models table](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/fine-tuning-considerations)
before you plan a fine-tuning project.

</div>
</details>

## Deploy a base model

First, deploy the model you'll fine-tune — and use as the baseline to compare against.

1. On the **Discover** page, select the **Models** tab to view the Microsoft Foundry model catalog.
1. In the model catalog, search for `gpt-4.1`.
1. Review the model card, and then deploy it using the default settings.
1. When the model has been deployed, it will open in the model playground.

## Start the fine-tuning job

Because fine-tuning takes some time to complete, you'll start the job now and come back to it
after exploring the base `gpt-4.1` model you just deployed.

1. Download the [training dataset](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/main/labfiles/A-choose-evaluate-and-safeguard-a-model/data/wingtip-finetune-train.jsonl) at:

    ```
    https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/main/labfiles/A-choose-evaluate-and-safeguard-a-model/data/wingtip-finetune-train.jsonl
    ```

    Save it as a JSONL file locally.

    > **Note**: Your device might default to saving the file as a .txt file. Select all files and remove the .txt suffix to ensure you're saving the file as JSONL.

1. In the Foundry portal, while viewing the model playground, in the left navigation pane, select **Fine-tune**.
1. Select the **Fine-tune** button at the upper right, and then configure the fine-tuning job with the following settings:
    - **Base model**: Select **gpt-4.1**
    - **Customization method**: Supervised
    - **Training type**: Standard
    - **Training data**: Select **Upload new dataset** and upload the .jsonl file you downloaded previously.
    - **Suffix**: `ft-wingtip`
    - **Automatically deploy model after job completion**: Selected
    - **Deployment type**: Developer
    - *Leave the remaining hyperparameters at their defaults*
1. Select **Submit** to start the fine-tuning job. It may take some time to complete. You can continue with the next section of the exercise while you wait.

> **Note**: Fine-tuning and deployment can take a significant amount of time (60 minutes or longer), so you may need to check back periodically. You can see more details of the progress so far by selecting the fine-tuning job and viewing its **Monitor** tab.

## Chat with the base model

While you wait for the fine-tuning job to complete, let's chat with the base `gpt-4.1` model
to assess how it performs.

1. In the left pane, select **Deployments** and then select the **gpt-4.1** base model you deployed previously.
1. In the chat pane, enter the prompt `What can you do?` and view the response.

    The answers may be fairly generic. Remember we want an assistant that inspires people to travel.

1. Change the model **Instructions** to the following prompt:

    ```
   You are the Wingtip Journeys AI assistant that helps people plan their travel.
    ```

1. In the chat window, enter the query `What can you do?` again, and view the response.

    As a response, the assistant may tell you that it can help you book flights, hotels and rental cars for your trip. Wingtip Journeys doesn't want this behavior — its assistant inspires, its consultants book.

1. In the **Instructions** field, enter a new prompt:

    ```
   You are the Wingtip Journeys AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms.
   You should not provide any hotel, flight, rental car or restaurant recommendations.
   Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday.
    ```

1. Continue testing the model to review its behavior. For example, ask the following questions and note the model's answers, paying particular attention to the tone and writing style that the model uses to respond:

    `Where in Rome should I stay?`

    `I'm mostly there for the food. Where should I stay to be within walking distance of affordable restaurants?`

    `What are some local delicacies I should try?`

    `When is the best time of year to visit in terms of the weather?`

    `What's the best way to get around the city?`

## Review the training file

The base model seems to work well enough, but you may be looking for a particular
conversational style from your generative AI app. The training data used for fine-tuning
offers you the chance to create explicit examples of the kinds of response you want.

1. Open the JSONL file you downloaded previously (you can open it in any text editor).
1. Examine the list of the JSON documents in the training data file. The first one should be similar to this (formatted for readability):

    ```json
    {"messages": [
        {"role": "system", "content": "You are the Wingtip Journeys AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms. You should not provide any hotel, flight, rental car or restaurant recommendations. Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday."},
        {"role": "user", "content": "What's a must-see in Paris?"},
        {"role": "assistant", "content": "Oh la la! You simply must twirl around the Eiffel Tower and snap a chic selfie! After that, consider visiting the Louvre Museum to see the Mona Lisa and other masterpieces. What type of attractions are you most interested in?"}
        ]}
    ```

    Each example interaction in the list includes the same system message you tested with the base model, a user prompt related to a travel query, and a response. The style of the responses in the training data will help the fine-tuned model learn how it should respond.

## Test the fine-tuned model

When your fine-tuned model is ready, you can test it like you tested your deployed base model.

1. In the pane on the left, select **Fine-tune** and review the status of the fine-tuning job you started earlier.
1. Select the job to view its details. You can use the **Logs** tab to review the fine-tuning tasks that have been performed so far.
1. When fine-tuning is complete, and the model has been automatically deployed, view the **Deployments** page to verify that it is listed.

    > **Tip**: If automatic deployment fails, select the completed fine-tuning job and deploy the model from there.
1. Select the fine-tuned model to open it in the model playground.
1. Update the **Instructions** to be the same as you tested with the base model:

    ```
   You are the Wingtip Journeys AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms.
   You should not provide any hotel, flight, rental car or restaurant recommendations.
   Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday.
    ```

1. Test your fine-tuned model to assess whether its behavior is more consistent than the base model. For example, ask the following questions again and explore the model's answers:

    `Where in Rome should I stay?`

    `I'm mostly there for the food. Where should I stay to be within walking distance of affordable restaurants?`

    `What are some local delicacies I should try?`

    `When is the best time of year to visit in terms of the weather?`

    `What's the best way to get around the city?`

> ✅ **Checkpoint**: You've fine-tuned a model on Wingtip Journeys training data and compared
> it, prompt for prompt, against the base model it came from.

**Stretch**: this lab ships a small validation set alongside the training data at
`labfiles/A-choose-evaluate-and-safeguard-a-model/data/wingtip-finetune-validation.jsonl`.
Re-run the fine-tuning job with it supplied as **Validation data** and compare the loss curves
on the job's **Monitor** tab.

> **Important**: A fine-tuned model deployment keeps incurring hosting charges until you delete
> it. When you're finished, follow the **Clean up** steps on the
> [lab overview](A-choose-evaluate-and-safeguard-a-model.md).

---

**Next:** You've completed the optional tasks. Head back to the
[lab overview](A-choose-evaluate-and-safeguard-a-model.md) for a summary and clean-up steps —
or continue into the companion lab,
[Build a generative AI chat app](B-build-a-generative-ai-chat-app.md), and put a model behind
real application code.
