---
lab:
    title: 'Create a generative AI app that uses your own data'
    description: 'Learn how to use the Retrieval Augmented Generation (RAG) model to build a chat app that grounds prompts using your own data.'
---

# Create a generative AI app that uses your own data

Retrieval Augmented Generation (RAG) is a technique used to build applications that integrate data from custom data sources into a prompt for a generative AI model. RAG is a commonly used pattern for developing generative AI apps - chat-based applications that use a language model to interpret inputs and generate appropriate responses.

In this exercise, you'll use Azure AI Foundry to integrate custom data into a generative AI solution.

This exercise takes approximately **45** minutes.

> **Note**: This exercise is based on pre-release services, which may be subject to change.

## Create an Azure AI Foundry resource

Let's start by creating an Azure AI Foundry resource.

1. In a web browser, open the [Azure portal](https://portal.azure.com) at `https://portal.azure` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in.
1. Create a new `Azure AI Foundry` resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Name**: *A valid name for your Azure AI Foundry resource*
    - **Region**: Choose one of the following regions:
        - East US 2
        - Sweden Central
    - **Default project name**: *A valid name for your project*

1. Wait for the resource to be created, then go to its page in the Azure portal.
1. In the page for your Azure AI Foundry resource, select **Go to Azure AI Foundry portal**.

## Deploy models

You need two models to implement your solution:

- An *embedding* model to vectorize text data for efficient indexing and processing.
- A model that can generate natural language responses to questions based on your data.

1. In the Azure AI Foundry portal, in your project, in the navigation pane on the left, under **My assets**, select the **Models + endpoints** page.
1. Create a new deployment of the **text-embedding-ada-002** model with the following settings by selecting **Customize** in the Deploy model wizard:

    - **Deployment name**: *A valid name for your model deployment*
    - **Deployment type**: Global Standard
    - **Model version**: *Select the default version*
    - **Connected AI resource**: *Select the resource created previously*
    - **Tokens per Minute Rate Limit (thousands)**: 50K *(or the maximum available in your subscription if less than 50K)*
    - **Content filter**: DefaultV2

    > **Note**: If your current AI resource location doesn't have quota available for the model you want to deploy, you will be asked to choose a different location where a new AI resource will be created and connected to your project.

1. Return to the **Models + endpoints** page and repeat the previous steps to deploy a **gpt-4o** model using a **Global Standard** deployment of the most recent version with a TPM rate limit of **50K** (or the maximum available in your subscription if less than 50K).

    > **Note**: Reducing the Tokens Per Minute (TPM) helps avoid over-using the quota available in the subscription you are using. 50,000 TPM is sufficient for the data used in this exercise.

## Add data to your project

The data for your app consists of a set of travel brochures in PDF format from the fictitious travel agency *Margie's Travel*. Let's add them to the project.

1. In a new browser tab, download the [zipped archive of brochures](https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip) from `https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip` and extract it to a folder named **brochures** on your local file system.
1. In Azure AI Foundry portal, in your project, in the navigation pane on the left, select **Playgrounds**, then select **Try the Chat playground**.
1. In the **Setup** pane of the playground, expand the **Add your data** section and select **Add a data source**.
1. In the **Add data** wizard, expand the drop-down menu to select **Upload files**.
1. Create a new Azure Blob storage resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Same resource group as your Azure AI Foundry resource*
    - **Storage account name**: *A valid name for your storage account resource*
    - **Region**: *Same region as your Azure AI Foundry resource*
    - **Performance**: Standard
    - **Redundancy**: LRS
1. Create your resource and wait until the deployment is complete.
1. Return to your Azure AI Foundry tab, refresh the list of Azure Blob storage resources and select the newly create account.

    > **Note**: If you receive a warning that Azure OpenAI needs your permission to access your resource, select **Turn on CORS**.

1. Create a new Azure AI Search resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Same resource group as your Azure AI Foundry resource*
    - **Service name**: *A valid name for your Azure AI Search resource*
    - **Region**: *Same region as your Azure AI Foundry resource*
    - **Pricing tier**: Basic

1. Create your resource and wait until the deployment is complete.
1. Return to your Azure AI Foundry tab, refresh the list of Azure AI Search resources and select the newly create account.
1. Name your index `brochures-index`.
1. Enable the option **Add vector search to this search resource** and select the embedding model you deployed earlier. Select **Next**.

   >**Note**: It might take a while until the **Add data** wizard recognizes your embedding model deployed, so if you can't enable the vector search option, cancel the wizard, wait a few minutes and try it again.

1. Upload all the .pdf files from the **brochures** folder that you extracted earlier and then select **Next**.
1. In the **Data management** step, select the search type **Hybrid (vector + keyword)** and chunk size of **1024**. Select **Next**.
1. In the **Data connection** step, select **API key** as the authentication type. Select **Next**.
1. Review all configuration steps and then select **Save and close**.
1. Wait for the indexing process to be completed, which can take a while depending on available compute resources in your subscription.

    > **Tip**: While you're waiting for the index to be created, why not take a look at the brochures you downloaded to get familiar with their contents?

## Test the index in the playground

Before using your index in a RAG-based prompt flow, let's verify that it can be used to affect generative AI responses.

1. In the Chat playground page, in the Setup pane, ensure that your **gpt-4o** model deployment is selected. Then, in the main chat session panel, submit the prompt `Where can I stay in New York?`
1. Review the response, which should be based on data in the index.

## Create a RAG client app

Now that you have a working index, you can use the Azure OpenAI SDK to implement the RAG pattern in a client application. Let's explore the code to accomplish this in a simple example.

> **Tip**: You can choose to develop your RAG solution using Python or Microsoft C#. Follow the instructions in the appropriate section for your chosen language.

### Prepare the application configuration

1. Return to the browser tab containing the Azure portal (keeping the Azure AI Foundry portal open in the existing tab).
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

    > **Tip**: As you paste commands into the cloudshell, the output may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. After the repo has been cloned, navigate to the folder containing the chat application code files:

    > **Note**: Follow the steps for your chosen programming language.

    **Python**

    ```
   cd mslearn-ai-foundry/labfiles/rag-app/python
    ```

    **C#**

    ```
   cd mslearn-ai-foundry/labfiles/rag-app/c-sharp
    ```

1. In the cloud shell command-line pane, enter the following command to install the OpenAI SDK library:

    **Python**

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install -r requirements.txt openai
    ```

    **C#**

    ```
   dotnet add package Azure.AI.OpenAI
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

1. In the code file, replace the following placeholders: 
    - **your_openai_endpoint**: The Open AI endpoint from your project's **Overview** page in the Azure AI Foundry portal (be suer the select the **Azure OpenAI** capability tab, not the Azure AI Inference or Azure AI Services capability).
    - **your_openai_api_key** The Open AI API key from your project's **Overview** page in the Azure AI Foundry portal (be suer the select the **Azure OpenAI** capability tab, not the Azure AI Inference or Azure AI Services capability).
    - **your_chat_model**: The name you assigned to your **gpt-4o** model deployment, from the **Models + endpoints** page in the Azure AI Foundry portal (the default name is `gpt-4o`).
    - **your_embedding_model**: The name you assigned to your **text-embedding-ada-002** model deployment, from the **Models + endpoints** page in the Azure AI Foundry portal (the default name is `text-embedding-ada-002`).
    - **your_search_endpoint**: The URL for your Azure AI Search resource. You'll find this in the **Management center** in the Azure AI Foundry portal.
    - **your_search_api_key**: The API key for your Azure AI Search resource. You'll find this in the **Management center** in the Azure AI Foundry portal.
    - **your_index**: Replace with your index name from the **Data + indexes** page for your project in the Azure AI Foundry portal (it should be `brochures-index`).
1. After you've replaced the placeholders, in the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

### Explore code to implement the RAG pattern

1. Enter the following command to edit the code file that has been provided:

    **Python**

    ```
   code rag-app.py
    ```

    **C#**

    ```
   code Program.cs
    ```

1. Review the code in the file, noting that it:
    - Creates an Azure OpenAI client using the endpoint, key, and chat model.
    - Creates a suitable system message for a travel-related chat solution.
    - Submits a prompt (including the system and a user message based on the user input) to the Azure OpenAI client, adding:
        - Connection details for the Azure AI Search index to be queried.
        - Details of the embedding model to be used to vectorize the query\*.
    - Displays the response from the grounded prompt.
    - Adds the response to the chat history.

    \* *The query for the search index is based on the prompt, and is used to find relevant text in the indexed documents. You can use a keyword-based search that submits the query as text, but using a vector-based search can be more efficient - hence the use of an embedding model to vectorize the query text before submitting it.*

1. Use the **CTRL+Q** command to close the code editor without saving any changes, while keeping the cloud shell command line open.

### Run the chat application

1. In the cloud shell command-line pane, enter the following command to run the app:

    **Python**

    ```
   python rag-app.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. When prompted, enter a question, such as `Where should I go on vacation to see architecture?` and review the response from your generative AI model.

    Note that the response includes source references to indicate the indexed data in which the answer was found.

1. Try a follow-up question, for example `Where can I stay there?`

1. When you're finished, enter `quit` to exit the program. Then close the cloud shell pane.

## Clean up

To avoid unnecessary Azure costs and resource utilization, you should remove the resources you deployed in this exercise.

1. If you've finished exploring Azure AI Foundry, return to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and sign in using your Azure credentials if necessary. Then delete the resources in the resource group where you provisioned your Azure AI Search and Azure AI resources.
