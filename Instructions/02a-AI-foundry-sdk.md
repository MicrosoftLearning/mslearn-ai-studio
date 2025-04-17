---
lab:
    title: 'Create a generative AI chat app'
    description: 'Learn how to use the Azure AI Foundry SDK to build an app that connects to your project and chats with a language model.'
---

# Create a generative AI chat app

In this exercise, you use the Azure AI Foundry SDK to create a simple chat app that connects to a project and chats with a language model.

This exercise takes approximately **40** minutes.

> **Note**: This exercise is based on pre-release SDKs, which may be subject to change. Where necessary, we've used specific versions of packages; which may not reflect the latest available versions. You may experience some unexpected behavior, warnings, or errors.

## Create an Azure AI Foundry project

Let's start by creating an Azure AI Foundry project.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Azure AI Foundry** logo at the top left to navigate to the home page, which looks similar to the following image (close the **Help** pane if it's open):

    ![Screenshot of Azure AI Foundry portal.](./media/ai-foundry-home.png)

1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a valid name for your project and if an existing hub is suggested, choose the option to create a new one. Then review the Azure resources that will be automatically created to support your hub and project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A valid name for your hub*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: Select **Help me choose** and then select **gpt-4o** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource*
    - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.
1. When your project is created, close any tips that are displayed and review the project page in Azure AI Foundry portal, which should look similar to the following image:

    ![Screenshot of a Azure AI project details in Azure AI Foundry portal.](./media/ai-foundry-project.png)

## Deploy a generative AI model

Now you're ready to deploy a generative AI language model to support your chat application. In this example, you'll use the OpenAI gpt-4o model; but the principles are the same for any model.

1. In the toolbar at the top right of your Azure AI Foundry project page, use the **Preview features** (**&#9215;**) icon to ensure that the **Deploy models to Azure AI model inference service** feature is enabled. This feature ensures your model deployment is available to the Azure AI Inference service, which you'll use in your application code.
1. In the pane on the left for your project, in the **My assets** section, select the **Models + endpoints** page.
1. In the **Models + endpoints** page, in the **Model deployments** tab, in the **+ Deploy model** menu, select **Deploy base model**.
1. Search for the **gpt-4o** model in the list, and then select and confirm it.
1. Deploy the model with the following settings by selecting **Customize** in the deployment details:
    - **Deployment name**: *A valid name for your model deployment*
    - **Deployment type**: Global Standard
    - **Automatic version update**: Enabled
    - **Model version**: *Select the most recent available version*
    - **Connected AI resource**: *Select your Azure OpenAI resource connection*
    - **Tokens per Minute Rate Limit (thousands)**: 50K *(or the maximum available in your subscription if less than 50K)*
    - **Content filter**: DefaultV2

    > **Note**: Reducing the TPM helps avoid over-using the quota available in the subscription you are using. 50,000 TPM should be sufficient for the data used in this exercise. If your available quota is lower than this, you will be able to complete the exercise but you may experience errors if the rate limit is exceeded.

1. Wait for the deployment to complete.

## Create a client application to chat with the model

Now that you have deployed a model, you can use the Azure AI Foundry and Azure AI Model Inference SDKs to develop an application that chats with it.

> **Tip**: You can choose to develop your solution using Python or Microsoft C#. Follow the instructions in the appropriate section for your chosen language.

### Prepare the application configuration

1. In the Azure AI Foundry portal, view the **Overview** page for your project.
1. In the **Project details** area, note the **Project connection string**. You'll use this connection string to connect to your project in a client application.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab). Then in the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.

    Close any welcome notifications to see the Azure portal home page.

1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment with no storage in your subscription.

    The cloud shell provides a command-line interface in a pane at the bottom of the Azure portal. You can resize or maximize this pane to make it easier to work in.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    **<font color="red">Ensure you've switched to the classic version of the cloud shell before continuing.</font>**

1. In the cloud shell pane, enter the following commands to clone the GitHub repo containing the code files for this exercise (type the command, or copy it to the clipboard and then right-click in the command line and paste as plain text):

    ```
    rm -r mslearn-ai-foundry -f
    git clone https://github.com/microsoftlearning/mslearn-ai-studio mslearn-ai-foundry
    ```

    > **Tip**: As you enter commands into the cloudshell, the output may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. After the repo has been cloned, navigate to the folder containing the chat application code files:

    Use the command below depending on your choice of programming language.

    **Python**

    ```
   cd mslearn-ai-foundry/labfiles/chat-app/python
    ```

    **C#**

    ```
   cd mslearn-ai-foundry/labfiles/chat-app/c-sharp
    ```

1. In the cloud shell command-line pane, enter the following command to install the libraries you'll use:

    **Python**

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install python-dotenv azure-identity azure-ai-projects azure-ai-inference
    ```

    **C#**

    ```
   dotnet add package Azure.Identity
   dotnet add package Azure.AI.Projects --version 1.0.0-beta.3
   dotnet add package Azure.AI.Inference --version 1.0.0-beta.3
    ```
    

1. Enter the following command to edit the configuration file that has been provided:

    **Python**

    ```
   code .env
    ```

    **C#**

    ```
   code appsettings.json
    ```

    The file is opened in a code editor.

1. In the code file, replace the **your_project_connection_string** placeholder with the connection string for your project (copied from the project **Overview** page in the Azure AI Foundry portal), and the **your_model_deployment** placeholder with the name you assigned to your gpt-4 model deployment.
1. After you've replaced the placeholders, within the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

### Write code to connect to your project and chat with your model

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. Enter the following command to edit the code file that has been provided:

    **Python**

    ```
   code chat-app.py
    ```

    **C#**

    ```
   code Program.cs
    ```

1. In the code file, note the existing statements that have been added at the top of the file to import the necessary SDK namespaces. Then, find the comment **Add references**, and add the following code to reference the namespaces in the libraries you installed previously:

    **Python**

    ```python
   # Add references
   from dotenv import load_dotenv
   from azure.identity import DefaultAzureCredential
   from azure.ai.projects import AIProjectClient
   from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
    ```

    **C#**

    ```csharp
   // Add references
   using Azure.Identity;
   using Azure.AI.Projects;
   using Azure.AI.Inference;
    ```

1. In the **main** function, under the comment **Get configuration settings**, note that the code loads the project connection string and model deployment name values you defined in the configuration file.
1. Find the comment **Initialize the project client**, and add the following code to connect to your Azure AI Foundry project using the Azure credentials you're currently signed in with:

    > **Tip**: Be careful to maintain the correct indentation level for your code.

    **Python**

    ```python
   # Initialize the project client
   projectClient = AIProjectClient.from_connection_string(
        conn_str=project_connection,
        credential=DefaultAzureCredential())
    ```

    **C#**

    ```csharp
   // Initialize the project client
   var projectClient = new AIProjectClient(project_connection,
                        new DefaultAzureCredential());
    ```

1. Find the comment **Get a chat client**, and add the following code to create a client object for chatting with a model:

    **Python**

    ```python
   # Get a chat client
   chat = projectClient.inference.get_chat_completions_client()
    ```

    **C#**

    ```csharp
   // Get a chat client
   ChatCompletionsClient chat = projectClient.GetChatCompletionsClient();
    ```

    > **Note**: This code uses the Azure AI Foundry project client to create a secure connection to the default Azure AI Model Inference service endpoint associated with your project. You can also connect *directly* to the endpoint by using the Azure AI Model Inference SDK, specifying the endpoint URI displayed for the service connection in the Azure AI Foundry portal or in the corresponding Azure AI Services resource page in the Azure portal, and using an authentication key or Entra credential token. For more information about connecting to the Azure AI Model Inferencing service, see [Azure AI Model Inference API](https://learn.microsoft.com/azure/machine-learning/reference-model-inference-api).

1. Find the comment **Initialize prompt with system message**, and add the following code to initialize a collection of messages with a system prompt.

    **Python**

    ```python
   # Initialize prompt with system message
   prompt=[
            SystemMessage("You are a helpful AI assistant that answers questions.")
        ]
    ```

    **C#**

    ```csharp
   // Initialize prompt with system message
   var prompt = new List<ChatRequestMessage>(){
                    new ChatRequestSystemMessage("You are a helpful AI assistant that answers questions.")
                };
    ```

1. Note that the code includes a loop to allow a user to input a prompt until they enter "quit". Then in the loop section, find the comment **Get a chat completion** and add the following code to add the user input to the prompt, retrieve the completion from your model, and add the completion to the prompt (so that you retain chat history for future iterations):

    **Python**

    ```python
   # Get a chat completion
   prompt.append(UserMessage(input_text))
   response = chat.complete(
        model=model_deployment,
        messages=prompt)
   completion = response.choices[0].message.content
   print(completion)
   prompt.append(AssistantMessage(completion))
    ```

    **C#**

    ```csharp
   // Get a chat completion
   prompt.Add(new ChatRequestUserMessage(input_text));
   var requestOptions = new ChatCompletionsOptions()
   {
       Model = model_deployment,
       Messages = prompt
   };

   Response<ChatCompletions> response = chat.Complete(requestOptions);
   var completion = response.Value.Content;
   Console.WriteLine(completion);
   prompt.Add(new ChatRequestAssistantMessage(completion));
    ```

1. Use the **CTRL+S** command to save your changes to the code file.

### Run the chat application

1. In the cloud shell command-line pane, under the code editor, enter the following command to run the app:

    **Python**

    ```
   python chat-app.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. When prompted, enter a question, such as `What is the fastest animal on Earth?` and review the response from your generative AI model.
1. Try some follow-up questions, like `Where can I see one?` or `Are they endangered?`. The conversation should continue, using the chat history as context for each iteration.
1. When you're finished, enter `quit` to exit the program.

> **Tip**: If the app fails because the rate limit is exceeded. Wait a few seconds and try again. If there is insufficient quota available in your subscription, the model may not be able to respond.

## Use the OpenAI SDK

Your client app is built using the Azure AI Model Inference SDK, which means it can be used with any model deployed to the Azure AI Model Inference service. The model you deployed is an OpenAI GPT model, which you can also consume using the OpenAI SDK.

Let's make a few code modifications to see how to implement a chat application using the OpenAI SDK.

1. In the cloud shell command line for your code folder (*python* or *c-sharp*), enter the following command to install the required package:

    **Python**

    ```
   pip install openai
    ```

    **C#**

    ```
   dotnet add package Azure.AI.Projects --version 1.0.0-beta.6
   dotnet add package Azure.AI.OpenAI --prerelease
    ```

> **Note**: A different pre-release version of the Azure.AI.Projects package is required as an interim workaround for some incompatibilities with the Azure AI Model Inference SDK.

1. If your code file (*chat-app.py* or *Program.cs*) isn't already open, enter the following command to open it in the code editor:

    **Python**

    ```
   code chat-app.py
    ```

    **C#**

    ```
   code Program.cs
    ```

1. At the top of the code file, add the following reference(s):

    **Python**

    ```python
   import openai
    ```

    **C#**

    ```csharp
   using OpenAI.Chat;
   using Azure.AI.OpenAI;
    ```

1. Find the comment **Get a chat client**, and modify the code used to create a client object as follows:

    **Python**

    ```python
   # Get a chat client 
   openai_client = projectClient.inference.get_azure_openai_client(api_version="2024-10-21")
    ```

    **C#**

    ```csharp
   // Get a chat client
   ChatClient openaiClient = projectClient.GetAzureOpenAIChatClient(model_deployment);
    ```

    > **Note**: This code uses the Azure AI Foundry project client to create a secure connection to the default Azure OpenAI service endpoint associated with your project. You can also connect *directly* to the endpoint by using the Azure OpenAI SDK, specifying the endpoint URI displayed for the service connection in the Azure AI Foundry portal or in the corresponding Azure OpenAI or AI Services resource page in the Azure portal, and using an authentication key or Entra credential token. For more information about connecting to the Azure OpenAI service, see [Azure OpenAI supported programming languages](https://learn.microsoft.com/azure/ai-services/openai/supported-languages).

1. Find the comment **Initialize prompt with system message**, and modify the code to initialize a collection of messages with a system prompt as follows:

    **Python**

    ```python
   # Initialize prompt with system message
   prompt=[
        {"role": "system", "content": "You are a helpful AI assistant that answers questions."}
    ]
    ```

    **C#**

    ```csharp
   // Initialize prompt with system message
    var prompt = new List<ChatMessage>(){
        new SystemChatMessage("You are a helpful AI assistant that answers questions.")
    };
    ```

1. Find the comment **Get a chat completion** and modify the code to add the user input to the prompt, retrieve the completion from your model, and add the completion to the prompt as follows:

    **Python**

    ```python
   # Get a chat completion
   prompt.append({"role": "user", "content": input_text})
   response = openai_client.chat.completions.create(
        model=model_deployment,
        messages=prompt)
   completion = response.choices[0].message.content
   print(completion)
   prompt.append({"role": "assistant", "content": completion})
    ```

    **C#**

    ```csharp
   // Get a chat completion
   prompt.Add(new UserChatMessage(input_text));
   ChatCompletion completion = openaiClient.CompleteChat(prompt);
   var completionText = completion.Content[0].Text;
   Console.WriteLine(completionText);
   prompt.Add(new AssistantChatMessage(completionText));
    ```

1. Use the **CTRL+S** command to save your changes to the code file.

1. In the cloud shell command-line pane, under the code editor, enter the following command to run the app:

    **Python**

    ```
   python chat-app.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. Test the app by submitting questions as before. When you're finished, enter `quit` to exit the program.

    > **Note**: The Azure AI Model Inference SDK and OpenAI SDKs use similar classes and code constructs, so the code required minimal changes. You can use the Azure AI Model Inference SDK with *any* model that is deployed to an Azure AI Model Inference service endpoint. The OpenAI SDK only works with OpenAI models, but you can use it for models deployed to either an Azure AI Model Inference service endpoint or to an Azure OpenAI endpoint.  

## Summary

In this exercise, you used the Azure AI Foundry, Azure AI Model Inference, and Azure OpenAI SDKs to create a client application for a generative AI model that you deployed in an Azure AI Foundry project.

## Clean up

If you've finished exploring Azure AI Foundry portal, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
