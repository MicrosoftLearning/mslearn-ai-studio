---
lab:
    title: 'Create a generative AI chat app with the Microsoft Foundry SDK'
    description: 'Learn how to use the Responses API and Microsoft Foundry to build a chat app that connects to your project and chats with a language model.'
    level: 300
    duration: 45
---

# Create a generative AI chat app with the Microsoft Foundry SDK

In this exercise, you use the Microsoft Foundry SDK and the Responses API to create a simple chat app that connects to a Microsoft Foundry project and chats with a language model.

This exercise takes approximately **45** minutes.

## Prerequisites

To complete this exercise, you need:

- An [Azure subscription](https://azure.microsoft.com/free/) with permissions to create AI resources.
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine.
- [Python 3.13](https://www.python.org/downloads/) or later installed on your local machine.
- [Git](https://git-scm.com/downloads) installed on your local machine.
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed on your local machine.

## Create a Microsoft Foundry project

Let's start by creating a project and deploying a model.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. Select the project name in the upper-left corner, and then select **Create new project**.
1. Enter a valid name for your project and select **Advanced options** to configure:
    - **Resource group**: *Create a new resource group or select an existing one*
    - **Location**: *Select a region close to you*\*

    > \* Some resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Create project** and wait for it to be created. When the project overview page appears, your project is ready.

## Deploy a model

Now deploy a model that you'll use in your chat application.

1. In your project, select **Discover** in the upper-right navigation.
1. Select **Models**.
1. Search for **gpt-4.1**.
1. Select the **gpt-4.1** model, and then select **Deploy** > **Default settings** to add it to your project.

    > <font color="red"><b>IMPORTANT</b>:</font> Depending on your available quota for gpt-4.1 models you might receive an additional prompt to deploy the model to a resource in a different region. If this happens, do so using the default settings.

1. Note the deployment name (for example, `gpt-4.1`). You'll need this name later.

## Create a client application to chat with the model

Now that you have deployed a model, you can use the Microsoft Foundry SDK and the Responses API to develop an application that chats with it.

### Prepare the application configuration

1. In the Microsoft Foundry portal, go to the **Overview** page for your project (the project welcome screen).
1. Find the **Foundry endpoint** displayed on the welcome screen (for example, `https://<your-resource>.services.ai.azure.com/api/projects/<your-project>`). Copy this endpoint — you'll use it to connect to your model.

    > **Note**: The Microsoft Foundry SDK handles authentication and endpoint routing automatically when you use `AIProjectClient.get_openai_client()`. Make a note of this endpoint.

1. Open **Visual Studio Code** on your local computer. If you don't have it installed, download it from [https://code.visualstudio.com](https://code.visualstudio.com).
1. Open a terminal in VS Code (**Terminal > New Terminal**) and clone the GitHub repo containing the code files for this exercise:

    ```
    git clone https://github.com/microsoftlearning/mslearn-ai-studio mslearn-ai-foundry
    ```

1. After the repo has been cloned, open the folder in VS Code (**File > Open Folder**), and navigate to the `mslearn-ai-foundry/labfiles/foundry-chat/python` folder.
1. In the VS Code Explorer pane, review the files in the folder:

    - `.env` - A configuration file for application settings.
    - `chat-app.py` - The Python code file for the chat application.
    - `requirements.txt` - A file listing the package dependencies.

1. Open a terminal in VS Code and navigate to the project folder, then install the required libraries:

    ```
    cd mslearn-ai-foundry/labfiles/foundry-chat/python
    python -m venv labenv
    ```

1. Activate the virtual environment:

    ```
    labenv\Scripts\activate
    ```

1. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

1. In VS Code, open the `.env` file and replace the placeholders:
    - Replace **your_foundry_endpoint** with the Foundry endpoint you copied from the project overview page.
    - Replace **your_model_deployment** with the name of your gpt-4.1 model deployment (for example, `gpt-4.1`).

    > <font color="red"><b>IMPORTANT</b>:</font> If you deployed your gpt-4.1 model to a different region due to insufficient quota, on the <b>Models + Endpoints</b> page, select your model and use its <b>Target URI</b> as your endpoint instead.

1. Save the `.env` file.

### Write code to connect to your project and chat with your model

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. In VS Code, open the `chat-app.py` file.
1. In the code file, note the existing statements that have been added at the top of the file to import the necessary packages. Then, find the comment **Add references**, and add the following code to reference the libraries you installed:

    ```python
    # Add references
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    ```

1. In the **main** function, under the comment **Get configuration settings**, note that the code loads the Foundry endpoint and model deployment name values you defined in the configuration file.
1. Find the comment **Initialize the project client**, and add the following code to connect to your Microsoft Foundry project:

    > **Tip**: Be careful to maintain the correct indentation level for your code.

    ```python
    # Initialize the project client
    project_client = AIProjectClient(
        endpoint=foundry_endpoint,
        credential=DefaultAzureCredential(),
    )
    ```

1. Find the comment **Get an OpenAI client from the project**, and add the following code to get an authenticated OpenAI client from your project:

    ```python
    # Get an OpenAI client from the project
    openai_client = project_client.get_openai_client()
    ```

1. Note that the code includes a loop to allow a user to input a prompt until they enter "quit", and it tracks conversation state using `previous_response_id`. Find the comment **Get a response** and add the following code to send the user input to your model using the Responses API and display the response:

    ```python
    # Get a response
    response = openai_client.responses.create(
        model=model_deployment,
        instructions="You are a helpful AI assistant that answers questions.",
        input=input_text,
        previous_response_id=previous_response_id
    )
    print(response.output_text)
    previous_response_id = response.id
    ```

    > **Note**: The Responses API uses `previous_response_id` to maintain conversation history automatically, so you don't need to manually track a messages array. The `instructions` parameter serves as the system message. Note that when using `previous_response_id`, instructions are not carried over from previous responses — they must be included in each call.

1. Save the file (**Ctrl+S**).

### Sign into Azure and run the app

1. In the VS Code terminal, sign into Azure:

    ```
    az login
    ```

    **<font color="red">You must sign into Azure to authenticate with your Microsoft Foundry project.</font>**

    > **Note**: In most scenarios, just using *az login* will be sufficient. However, if you have subscriptions in multiple tenants, you may need to specify the tenant by using the *--tenant* parameter. See [Sign into Azure interactively using the Azure CLI](https://learn.microsoft.com/cli/azure/authenticate-azure-cli-interactively) for details.

1. When prompted, follow the instructions to open the sign-in page in a new tab and enter the authentication code provided and your Azure credentials. Then complete the sign in process in the terminal, selecting the subscription containing your Foundry resource if prompted.
1. After you have signed in, run the application:

    ```
    python chat-app.py
    ```

1. When prompted, enter a question, such as `What is the fastest animal on Earth?` and review the response from your generative AI model.
1. Try some follow-up questions, like `Where can I see one?` or `Are they endangered?`. The conversation should continue, using the Responses API to maintain conversation context automatically.
1. When you're finished, enter `quit` to exit the program.

> **Tip**: If the app fails because the rate limit is exceeded. Wait a few seconds and try again. If there is insufficient quota available in your subscription, the model may not be able to respond.

## Customize the system instructions

The `instructions` parameter controls the persona and behavior of the model. Let's experiment with changing it.

1. In VS Code, open the `chat-app.py` file.
1. Find the `instructions` parameter in the `openai_client.responses.create(...)` call and change it from the default to a more specific persona:

    ```python
    instructions="You are a friendly travel guide who loves sharing fun facts about destinations around the world. Keep your answers engaging and suggest related places to visit.",
    ```

1. Save the file and run the application again:

    ```
    python chat-app.py
    ```

1. Try asking questions like `Tell me about Paris` or `Where should I go on vacation in South America?` and notice how the model's tone and content reflect the travel guide persona.
1. Feel free to experiment with other instructions — for example, a cooking tutor, a fitness coach, or a historical storyteller. Notice how the same model produces very different responses based on the instructions you provide.
1. When you're done experimenting, enter `quit` to exit the program.

    > **Note**: Remember that the `instructions` parameter is sent with every call when using `previous_response_id` — it's not carried over from prior responses. This means you can even change the persona mid-conversation if you want.

## Add streaming responses

So far, the app waits for the entire response to be generated before displaying it. In production applications, streaming delivers a much better user experience by displaying text as it's generated — just like you see in ChatGPT and other AI chat interfaces.

1. In VS Code, open the `chat-app.py` file.
1. Find the current **Get a response** code block and replace it with the following streaming version:

    ```python
    # Get a response
    stream = openai_client.responses.create(
        model=model_deployment,
        instructions="You are a helpful AI assistant that answers questions.",
        input=input_text,
        previous_response_id=previous_response_id,
        stream=True
    )
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")
        elif event.type == "response.completed":
            previous_response_id = event.response.id
    print()
    ```

    > **Note**: The key changes are: adding `stream=True` to the API call, iterating over events to print text deltas as they arrive, and extracting `previous_response_id` from the `response.completed` event at the end of the stream.

1. Save the file and run the application again:

    ```
    python chat-app.py
    ```

1. Ask a question and observe how the response now appears word-by-word instead of all at once. This streaming pattern is essential for production chat applications where responsiveness matters.
1. When you're finished, enter `quit` to exit the program.

## Summary

In this exercise, you used the Microsoft Foundry SDK and the Responses API to create a client application for a generative AI model that you deployed in a Microsoft Foundry project. You customized the model's behavior using system instructions, and implemented streaming to deliver a responsive chat experience. The Responses API simplifies multi-turn conversations by automatically tracking conversation history through `previous_response_id`, eliminating the need to manually manage a messages array.

## Clean up

If you've finished exploring the Microsoft Foundry portal, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
