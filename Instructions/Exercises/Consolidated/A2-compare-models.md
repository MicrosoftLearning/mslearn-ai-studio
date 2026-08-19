---
lab:
    title: 'Task 2 – Compare models in the catalog and playground'
    description: 'Use model cards, benchmarks, the model leaderboard, and a side-by-side playground comparison to choose between two models for the Wingtip Journeys assistant.'
    level: 200
    concepts: 'model catalog, benchmarks, model leaderboard, side-by-side comparison'
    islab: true
    status: 'draft'
---

# Task 2 — Compare models in the catalog and playground

*Part of the **Choose, evaluate, and safeguard a model** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project**. Don't have one yet? Complete
> [Getting started](A0-getting-started.md) first. This task is completed entirely in the
> portal — no local code or configuration is required. You'll deploy two models during the
> task, so you don't need an existing deployment to begin.

> **Continuing from a previous task?** If you just finished
> [Task 1](A1-create-a-project-and-deploy-a-model.md) you already have `gpt-5.2` deployed —
> skip the "Deploy the gpt-5.2 model" step below and deploy only `gpt-5-mini`.

---

Wingtip Journeys wants the travel assistant to feel premium, but it also has to be affordable
to run at scale. That's a trade-off, and the model catalog is built for making trade-offs
visible.

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
<summary>What is a benchmark, and how much should I trust it?</summary>
<div class="concept-body" markdown="1">

A benchmark is a standard test set that every model is scored against, so scores are
comparable across models. Foundry surfaces quality, safety, cost, and throughput benchmarks
on model cards and in the leaderboard.

Benchmarks are an excellent *filter* and a poor *decision*. They tell you which models are
plausible for your scenario; they can't tell you which one is best on *your* prompts and
*your* data. That's what the playground comparison in this task — and the evaluation run in
[Task 4](A4-evaluate-a-model.md) — are for.

</div>
</details>

## Explore models in the catalog

Microsoft Foundry Models provides a catalog of models that you can use in your project. You can browse the catalog and compare models to find the right one for your needs.

1. Now you're ready to explore models. On the **Discover** page, select the **Models** tab to view the Microsoft Foundry model catalog.

    The model catalog lists all models available in Foundry. Some are provided directly from Azure (and billed through your Azure subscription) while others are provided by partners and the community.

    Note that you can search and filter the catalog, based on model names, capabilities, and other factors.

1. Search for `gpt-5.2`. Then, in the search results, select the **gpt-5.2** model to view its *model card*. Model cards provide information about models to help you determine if they are suitable for your needs.
1. Read the description and review the other information available on the **Details** page.
1. View the **Benchmarks** page for the gpt-5.2 model to see how the model compares across some standard performance benchmarks with other models that are used in similar scenarios.
1. Use the back arrow (**&larr;**) next to the **gpt-5.2** page title to return to the model catalog.

## Compare models using the model leaderboard

Now let's use the model leaderboard and side-by-side comparison features to compare models visually.

1. In the model catalog page, select **View leaderboard**.
1. In the **Model leaderboard** page, review the top models ranked by quality, safety, cost, and performance. Note which models score highest for AI quality metrics.
1. Scroll down to use the **Trade-off chart** section to compare models on multiple dimensions.
1. Select the **Benchmark Cost** from the dropdown to see how model quality relates to cost, and then use the model list to compare **gpt-5.2** and **gpt-5-mini**. If you want to explore further, you can add other models to the comparison.

    This is the Wingtip Journeys trade-off in one chart: how much quality would you give up to
    halve the cost of every traveler conversation?

1. Select the **Throughput** metric from the dropdown to see how the quality of these models relates to throughput scores.
1. Select the **Safety** metric from the dropdown to see how the quality of these models relates to safety scores.
1. In the table just above the trade-off charts, you can compare benchmarks. Select **gpt-5.2** and **gpt-5-mini**, and optionally any other models you want to explore, and then use the **Compare models** button to view their benchmarks side-by-side.
1. Review the comparison across the following data:
    - **Performance benchmarks**: Quality, safety, and throughput scores.
    - **Input** and **output**: The formats supported for prompts and responses.
    - **Context**: The number of tokens that can be maintained in a conversation and produced as output, and when the model was trained.
    - **Endpoints**: The API endpoints through which the model can be consumed by client applications, and whether it can be used by an agent.
    - **Supported features**: Specific capabilities that you may require in your application scenario.
1. Use the back arrow (**&larr;**) next to the **gpt-5.2** page title to return to the model catalog.

## Deploy models

Now let's deploy the models we'll use for testing. You need to deploy **gpt-5.2** and **gpt-5-mini**.

### Deploy the gpt-5.2 model

> Already deployed `gpt-5.2` in Task 1? Skip straight to *Deploy the gpt-5-mini model*.

1. In the model catalog, search for `gpt-5.2` and select it.
1. On the model page, select **Deploy** and deploy the model using the *default* settings.

    The deployed model will open in the model playground, where it will be selected in the **Model** drop-down list.

1. Note the deployment name that is assigned to the **gpt-5.2** model. You'll need to identify this deployment later.

### Deploy the gpt-5-mini model

1. In the model playground, in the **Model** list, select **Browse more models**.
1. Search for `gpt-5-mini`, and then select it and deploy it.

    The model is deployed and selected in the model playground.

1. Note the deployment name that is assigned to the **gpt-5-mini** model.

## Compare models in the model playground

Now that you have two model deployments, let's compare them in the playground.

1. In the playground, ensure the deployment for the **gpt-5-mini** model is selected in the **Models** list, and then on the right side of the page, in the **Compare models** list, select the deployment for the **gpt-5.2** model.
1. The side-by-side comparison view opens directly into separate chat panes for each model. Select the **Chat** tab for both models, and enter the following prompt:

    ```
   A Wingtip Journeys traveler has one carry-on bag, a fox terrier in a travel crate, and a sealed box of chocolates. The ferry to the island takes one passenger item per crossing. If the dog is left alone with the chocolates it will eat them, and if the bag is left alone with the dog it will chew through the bag. How can the traveler get all three across without anything being lost?
    ```

1. Submit the prompt and view the responses from both models. Then, enter the following follow-up prompt:

    ```
   Explain your reasoning.
    ```

1. Compare the responses from each model. Note any differences in accuracy, reasoning quality, and response style.

> ✅ **Checkpoint**: You've compared two candidate models on published benchmarks *and* on a
> prompt of your own, and you have both deployed in your project. That's enough evidence to
> shortlist one — and [Task 4](A4-evaluate-a-model.md) shows you how to prove it at scale.

**Stretch**: repeat the side-by-side comparison with a prompt drawn from real Wingtip Journeys
traveler questions, such as visa rules for a multi-country itinerary. Does the cheaper model
still hold up?

---

**Next (optional):** [Task 3 — Explore your project from Visual Studio Code](A3-explore-your-project-from-vs-code.md)
