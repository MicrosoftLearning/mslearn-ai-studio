---
lab:
    title: 'Getting started: set up your environment'
    description: 'Shared setup for the Build a generative AI chat app lab: create a Microsoft Foundry project, deploy a model, get the starter code, and configure your environment. Complete this once before any task.'
    level: 300
    concepts: 'environment setup, Microsoft Foundry project, Azure OpenAI endpoint'
    status: 'draft'
---

# Getting started

This page sets up everything the **Build a generative AI chat app** lab needs. **Every task
begins here** — complete this page first. Each task is written so you can then do it on its
own; if you're working through the whole lab in one sitting, you only need to do this setup
once.

**Your scenario:** you're the AI developer at **Wingtip Journeys**, a travel company that plans
small-group trips. Across the lab you'll build the client application behind the Wingtip
Journeys travel assistant, adding one capability per task.

> **Note**: Some of the technologies used in this lab are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

Before starting, ensure you have:

- An active [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account) with sufficient permissions and quota to provision Azure AI resources
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Python version **3.13.xx**](https://www.python.org/downloads/release/python-31312/) installed\*
- [Git](https://git-scm.com/install/) installed and configured
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli?view=azure-cli-latest) installed

> \* Python 3.14 is available, but some dependencies are not yet compiled for that release. The lab has been successfully tested with Python 3.13.12.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` to start building; signing in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in.

1. If it is not already enabled, in the tool bar at the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name (for example, `wingtip-journeys`); expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any of the **AI Foundry recommended** regions in **[this list](https://learn.microsoft.com/azure/foundry/openai/how-to/responses#region-availability)**{:target="_blank"}

1. Wait for your project to be created. Then view its home page.

> **Already completed the companion lab?** If you finished
> [Choose, evaluate, and safeguard a model](A-choose-evaluate-and-safeguard-a-model.md), reuse
> that project and its `gpt-5.2` deployment — skip straight to *Get the endpoint*.

## Deploy a model

Next, let's deploy the model your chat application will use.

1. On the **Discover** page, select the **Models** tab to view the Microsoft Foundry model catalog.
1. In the model catalog, search for `gpt-5.2`.
1. Review the model card, and then deploy it using the default settings.
1. When the model has been deployed, it will open in the model playground — you can test it there if you like.
1. Note the **deployment name** that is assigned. You'll put it in your `.env` file shortly.

## Get the endpoint

You'll need an endpoint to connect to the model from a client application. In this lab, we're
going to use the OpenAI SDK to chat with the model; and we'll use the Azure OpenAI endpoint
with Entra ID authentication to connect to it.

> **Note**: As an alternative to Entra ID authentication, you could use the API key for the project. Using Entra ID authentication is preferred whenever possible.

1. On the menu bar, select the **Home** page.
1. Note the **Azure OpenAI Endpoint** displayed there.

    > **Tip**: You'll use the **Azure OpenAI Endpoint** in this lab, <u>not</u> the project endpoint!

## Get the starter code

1. In Visual Studio Code, open the Command Palette (**Ctrl+Shift+P**), run **Git: Clone**, and enter:

    ```
    https://github.com/MicrosoftLearning/mslearn-ai-studio.git
    ```

    You may be prompted to confirm you trust the authors.

1. Open the cloned repo, then in the **Explorer** pane navigate to `labfiles/B-build-a-generative-ai-chat-app/python`. This single folder holds the starter code for **every** task in this lab — you use one virtual environment and one `.env` throughout. It contains:
    - **guides** (a folder of Wingtip Journeys destination guides, used in Task 4)
    - **.env** (the application configuration file)
    - **.env.example** (a template showing which settings are needed)
    - **requirements.txt** (the Python package dependencies that need to be installed)
    - **chat-app.py** (the chat application you build in Tasks 1 and 2)
    - **chat-async.py** (the asynchronous version you build in Task 3)
    - **tools-app.py** (the grounded application you build in Task 4)

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.

1. Right-click the **python** folder and select **Open in Integrated Terminal**. Then create a virtual environment and install packages:

    ```
    python -m venv labenv
    .\labenv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

    > **Note**: You may need to enable running scripts on your system. Ensure the terminal prompt is prefixed with **(labenv)** to indicate that the Python environment is active.

1. Open the **.env** file and set `AZURE_OPENAI_ENDPOINT` to the **Azure OpenAI Endpoint** you noted above, and `MODEL_DEPLOYMENT` to your model deployment name. Save the file.

## Sign in to Azure

Every task authenticates with Microsoft Entra ID, so sign in once per session from the same terminal:

```
az login
```

> **Note**: In most scenarios, just using `az login` will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the `--tenant` parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

## Check you're ready for a task

Each task needs specific values in your `.env`. Before starting a task, run the preflight
check **from the `python` folder** — the same folder your terminal and virtual environment are
already in. It reads your `.env` and tells you what (if anything) is missing:

```
python ../setup/check_env.py --task 2
```

Swap `2` for the task number you're about to start. That's it — head to any task:

| Task | Page |
| --- | --- |
| Task 1 – Chat with a model from code | [B1](B1-chat-with-a-model-from-code.md) |
| Task 2 – Keep context and stream responses | [B2](B2-keep-context-and-stream-responses.md) |
| Task 3 – Use the asynchronous API | [B3](B3-use-the-asynchronous-api.md) |
| Task 4 – Ground your app with file search and web search | [B4](B4-ground-your-app-with-tools.md) |
