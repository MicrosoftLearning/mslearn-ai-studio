---
lab:
    title: 'Getting started: set up your Foundry project'
    description: 'Shared setup for the Choose, evaluate, and safeguard a model lab: create a Microsoft Foundry project and deploy the model the Wingtip Journeys assistant runs on. Complete this once before any task.'
    level: 300
    concepts: 'environment setup, Microsoft Foundry project, model deployment'
    status: 'draft'
---

# Getting started

This page sets up everything the **Choose, evaluate, and safeguard a model** lab needs.
**Every task begins here** — complete this page first. Each task is written so you can then do
it on its own; if you're working through the whole lab in one sitting, you only need to do
this setup once.

**Your scenario:** you're the AI developer at **Wingtip Journeys**, a travel company that plans
small-group trips. Across the lab you'll choose, measure, safeguard, and tune the model that
powers the Wingtip Journeys travel assistant.

> **Note**: Some of the technologies used in this lab are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting, ensure you have:

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account) with sufficient permissions and quota to provision Azure AI resources

Two optional tasks need a little more:

- **Task 3 (VS Code)** also needs [Visual Studio Code](https://code.visualstudio.com/) installed.
- **Task 6 (fine-tuning)** needs a project in a region that supports fine-tuning, and the
  training dataset from this repo. Task 6 tells you exactly what to do — read its **What you
  need** callout *before* you create your project if you plan to complete it.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to
develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` to start building; signing in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in.

1. If it is not already enabled, in the tool bar at the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name (for example, `wingtip-journeys`); expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any of the **AI Foundry recommended** regions in **[this list](https://learn.microsoft.com/azure/foundry/openai/how-to/responses#region-availability)**{:target="_blank"}\*

    > \* **Planning to do Task 6 (fine-tuning)?** Choose **North Central US** or **Sweden Central**
    > instead — those regions support the fine-tuning method that task uses. Some Azure AI
    > resources are constrained by regional model quotas, so if you hit a quota limit later you
    > may need to create another resource in a different region.

    > **Tip**: Make a note of the region you selected. You'll need it later!

1. Select **Create**. Wait for your project to be created.

    When it is ready, the project home page will open.

    ![Screenshot of the Foundry project home page.](../../media/foundry-portal-home.png)

## Deploy a model

Every task in this lab needs at least one deployed model. Task 1 walks through this in detail,
including testing the model in the playground — if you're starting at Task 1, you can skip
ahead now and do it there.

If you're jumping straight to a later task, deploy the model here:

1. On the **Discover** page, select the **Models** tab to view the Microsoft Foundry model catalog.
1. Search for `gpt-5.2`, select it in the search results, and review its model card.
1. Select **Deploy** with the default settings to create a deployment of the model.
1. Note the **deployment name** that is assigned. Several tasks ask you to identify this deployment.

## Check you're ready for a task (optional)

Every task in this lab is completed in the portal, so you don't need to clone anything to work
through it. If you'd like a reminder of what a given task expects — and, for Task 6, a check
that the training data is valid — clone this repo and run the preflight script.

1. In Visual Studio Code, open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-studio.git
    ```

1. Open a terminal in the `labfiles/A-choose-evaluate-and-safeguard-a-model` folder of the cloned repo and run:

    ```
    python setup/check_env.py --task 4
    ```

Swap `4` for the task number you're about to start. The check reads local files only, never
calls Azure, and needs no installed packages beyond Python itself, so it's safe to run at any
time. (This lab is completed in the portal, so for most tasks the check simply confirms what
you need to have created there.)

> **Task 6 note**: Task 6 also gives you a direct download link for the training dataset, so
> you can complete it without cloning the repo at all.

That's it — head to any task:

| Task | Page |
| --- | --- |
| Task 1 – Create a project and deploy a model | [A1](A1-create-a-project-and-deploy-a-model.md) |
| Task 2 – Compare models in the catalog and playground | [A2](A2-compare-models.md) |
| Task 3 – Explore your project from Visual Studio Code | [A3](A3-explore-your-project-from-vs-code.md) |
| Task 4 – Evaluate a model with a synthetic dataset | [A4](A4-evaluate-a-model.md) |
| Task 5 – Apply guardrails to block harmful content | [A5](A5-apply-guardrails.md) |
| Task 6 – Fine-tune a model for a consistent voice | [A6](A6-fine-tune-a-model.md) |
