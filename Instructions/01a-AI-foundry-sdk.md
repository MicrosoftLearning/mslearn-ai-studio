---
lab:
    title: 'Create a chat app with the Azure AI Foundry SDK'
---

# Create a chat app with the Azure AI Foundry SDK

In this exercise, you use the Azure AI Foundry SDK to create a simple chat app.

This exercise takes approximately **20** minutes.

## Create an Azure AI Foundry project

Let's start by creating an Azure AI Foundry project.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Azure AI Foundry** logo at the top left to navigate to the home page, which looks similar to the following image:

    ![Screenshot of Azure AI Foundry portal.](./media/ai-foundry-home.png)

1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a suitable project name for (for example, `my-ai-project`) then review the Azure resources that will be automatically created to support your project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A unique name - for example `my-ai-hub`*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create a new resource group with a unique name (for example, `my-ai-resources`), or select an existing one*
    - **Location**: Choose a random region from the following list\*:
        - East US
        - East US 2
        - North Central US
        - South Central US
        - Sweden Central
        - West US
        - West US 3
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource with an appropriate name (for example, `my-ai-services`) or use an existing one*
    - **Connect Azure AI Search**: Skip connecting

    > \* Model quotas are constrained at the tenant level by regional quotas. Choosing a random region helps distribute quota availability when multiple users are working in the same tenant. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.
1. When your project is created, close any tips that are displayed and review the project page in Azure AI Foundry portal, which should look similar to the following image:

    ![Screenshot of a Azure AI project details in Azure AI Foundry portal.](./media/ai-foundry-project.png)

## Deploy a generative AI model

YNow you're ready to deploy a generative AI language model to support your chat application. In this example, you'll use the Microsoft Phi-4 model; but the principles are the same for any model.

1. In the pane on the left for your project, in the **My assets** section, select the **Models + endpoints** page.
1. In the **Models + endpoints** page, in the **Model deployments** tab, in the **+ Deploy model** menu, select **Deploy base model**.
1. Search for the **Phi-4** model in the list, and then select and confirm it.
1. Select the **Serverless API with Azure AI Content Safety** deployment option.
1. Deploy the model with the following settings by selecting **Customize** in the deployment details:
    - **Deployment name**: *A unique name for your model deployment - for example `phi-4-model` (remember the name you assign, you'll need it later*)
    - **Content filter**: Enabled

## Create a client application to chat with the model

Now that you have deployed a model, you can use the Azure AI Foundry SDK to develop an application that chats with it.

### Prepare the application configuration

1. In the Azure AI Foundry portal, view the **Overview** page for your project.
1. In the **Project details** area, note the **Project connection string**. You'll use this connection string to connect to your project in a client application.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab). Then in the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.
1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

1. In the PowerShell pane, enter the following commands to clone the GitHub repo for this exercise:

    ```
    rm -r mslearn-ai-foundry -f
    git clone https://github.com/microsoftlearning/mslearn-ai-studio mslearn-ai-foundry
    ```

1. After the repo has been cloned, navigate to the **mslearn-ai-foundry/labfiles/01a-azure-foundry-sdk/python** folder:

    ```
    cd mslearn-ai-foundry/labfiles/01a-azure-foundry-sdk/python
    ```

1. In the cloud shell command line pane, enter the following command to install the Python libraries you'll use, which are:
    - **python-dotenv** : Used to load settings from an application configuration file.
    - **azure-identity**: Used to authenticate with Entra ID credentials.
    - **azure-ai-projects**: Used to work with an Azure AI Foundry project.
    - **azure-ai-inference**: Used to chat with a generative AI model.

    ```
    pip install python-dotenv azure-identity azure-ai-projects azure-ai-inference
    ```

1. Enter the following command to edit the **.env** Python configuration file that has been provided:

    ```
    code .env
    ```

    The file is opened in a code editor.

1. In the code file, replace the **your_project_endpoint** placeholder with the connection string for your project (copied from the project **Overview** page in the Azure Ai Foundry portal), and the **your_model_deployment** placeholder with the name you assigned to your Phi-4 model deployment.
1. After you've replaced the placeholders, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

### Write code to connect to your project and chat with your model

> **Tip**: As you add code to the Python code file, be sure to maintain the correct indentation.

1. Enter the following command to edit the **chat-app.py** Python code file that has been provided:

    ```
    code chat-app.py
    ```

1. In the code file, note the existing **import** statements that have been added at the top of the file. Then, under the comment **# Add AI Projects reference**, add the following code to reference the Azure AI Projects library:

    ```python
    from azure.ai.projects import AIProjectClient
    ```

1. In the **main** function, under the comment **# Get configuration settings**, note that the code loads the project connection string and model deployment name values you defined in the **.env** file.
1. Under the comment **# Initialize the project client**, add the following code to connect to your Azure AI Foundry project using the Azure credentials you are currently signed in with:

    ```python
    project = AIProjectClient.from_connection_string(
        conn_str=project_connection,
        credential=DefaultAzureCredential()
        )
    ```
    
1. Under the comment **# Get a chat client**, add the following code to create a client object for chatting with a model:

    ```python
    chat = project.inference.get_chat_completions_client()
    ```

1. Note that the code includes a loop to allow a user to input a prompt until they enter "quit". Then in the loop section, under the comment **# Get a chat completion**, add the following code to submit the prompt and retrieve the completion from your model:

    ```python
    response = chat.complete(
        model=model_deployment,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant that answers questions."},
            {"role": "user", "content": input_text},
            ],
        )
    print(response.choices[0].message.content)
    ```

1. Use the **CTRL+S** command to save your changes to the code file and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

### Run the chat application

1. In the cloud shell command line pane, enter the following command to run the Python code:

    ```
    python chat-app.py
    ```

1. When prompted, enter a question, such as `What is the fastest animal on Earth?` and review the response from your generative AI model.
1. Try a few more questions. When you're finished, enter `quit` to exit the program.

## Summary

In this exercise, you used the Azure AI Foundry SDK to create a client application for a generative AI model that you deployed in an Azure AI Foundry project.

## Clean up

If you've finished exploring Azure AI Foundry portal, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
