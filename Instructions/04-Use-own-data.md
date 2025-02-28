---
lab:
    title: 'Create a generative AI app that uses your own data'
    description: 'Learn how to use the Retrieval Augmented Generation (RAG) model to build a chat app that grounds prompts using your own data.'
---

# Create a generative AI app that uses your own data

Retrieval Augmented Generation (RAG) is a technique used to build applications that integrate data from custom data sources into a prompt for a generative AI model. RAG is a commonly used pattern for developing generative AI apps - chat-based applications that use a language model to interpret inputs and generate appropriate responses.

In this exercise, you'll use Azure AI Foundry portal to integrate custom data into a generative AI prompt flow. You'll also explore how to implement the RAG pattern in a client app by using the Azure AI Foundry and Azure OpenAI SDKs.

This exercise takes approximately **45** minutes.

## Create an Azure AI Foundry project

Let's start by creating an Azure AI Foundry project and the service resources it needs to support using your own data - including an Azure AI Search resource.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Azure AI Foundry** logo at the top left to navigate to the home page, which looks similar to the following image:

    ![Screenshot of Azure AI Foundry portal.](./media/ai-foundry-home.png)

1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a suitable project name for (for example, `my-ai-project`) then review the Azure resources that will be automatically created to support your project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A unique name - for example `my-ai-hub`*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create a new resource group with a unique name (for example, `my-ai-resources`), or select an existing one*
    - **Location**: Select **Help me choose** and then select both **gpt-4** and **text-embedding-ada-002** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource with an appropriate name (for example, `my-ai-services`) or use an existing one*
    - **Connect Azure AI Search**: *Create a new Azure AI Search resource with a unique name*

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.
1. When your project is created, close any tips that are displayed and review the project **Overview** page in Azure AI Foundry portal, which should look similar to the following image:

    ![Screenshot of a Azure AI project details in Azure AI Foundry portal.](./media/ai-foundry-project.png)
   
## Deploy models

You need two models to implement your solution:

- An *embedding* model to vectorize text data for efficient indexing and processing.
- A model that can generate natural language responses to questions based on your data.

1. In the Azure AI Foundry portal, in your project, in the navigation pane on the left, under **My assets**, select the **Models + endpoints** page.
1. Create a new deployment of the **text-embedding-ada-002** model with the following settings by selecting **Customize** in the Deploy model wizard:

    - **Deployment name**: `text-embedding-ada-002`
    - **Deployment type**: Standard
    - **Model version**: *Select the default version*
    - **AI resource**: *Select the resource created previously*
    - **Tokens per Minute Rate Limit (thousands)**: 5K
    - **Content filter**: DefaultV2
    - **Enable dynamic quota**: Disabled

    > **Note**: If your current AI resource location doesn't have quota available for the model you want to deploy, you will be asked to choose a different location where a new AI resource will be created and connected to your project.

1. Repeat the previous steps to deploy a **gpt-4** model with the deployment name `gpt-4`.

    > **Note**: Reducing the Tokens Per Minute (TPM) helps avoid over-using the quota available in the subscription you are using. 5,000 TPM is sufficient for the data used in this exercise.

## Add data to your project

The data for your copilot consists of a set of travel brochures in PDF format from the fictitious travel agency *Margie's Travel*. Let's add them to the project.

1. Download the [zipped archive of brochures](https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip) from `https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip` and extract it to a folder named **brochures** on your local file system.
1. In Azure AI Foundry portal, in your project, in the navigation pane on the left, under **My assets**, select the **Data + indexes** page.
1. Select **+ New data**.
1. In the **Add your data** wizard, expand the drop-down menu to select **Upload files/folders**.
1. Select **Upload folder** and select the **brochures** folder.
1. Select **Next** and set the data name to `brochures`.
1. Wait for the folder to be uploaded and note that it contains several .pdf files.

## Create an index for your data

Now that you've added a data source to your project, you can use it to create an index in your Azure AI Search resource.

1. In Azure AI Foundry portal, in your project, in the navigation pane on the left, under **My assets**, select the **Data + indexes** page.
1. In the **Indexes** tab, add a new index with the following settings:
    - **Source location**:
        - **Data source**: Data in Azure AI Foundry portal
            - *Select the **brochures** data source*
    - **Index configuration**:
        - **Select Azure AI Search service**: *Select the **AzureAISearch** connection to your Azure AI Search resource*
        - **Vector index**: `brochures-index`
        - **Virtual machine**: Auto select
    - **Search settings**:
        - **Vector settings**: Add vector search to this search resource
        - **Azure OpenAI connection**: *Select the default Azure OpenAI resource for your hub.*

1. Wait for the indexing process to be completed, which can take several minutes. The index creation operation consists of the following jobs:

    - Crack, chunk, and embed the text tokens in your brochures data.
    - Create the Azure AI Search index.
    - Register the index asset.

## Test the index

Before using your index in a RAG-based prompt flow, let's verify that it can be used to affect generative AI responses.

1. In the navigation pane on the left, select the **Playgrounds** page.
1. On the Chat page, in the Setup pane, ensure that your **gpt-4** model deployment is selected. Then, in the main chat session panel, submit the prompt `Where can I stay in New York?`
1. Review the response, which should be a generic answer from the model without any data from the index.
1. In the Setup pane, expand the **Add your data** field, and then add the **brochures-index** project index and select the **hybrid (vector + keyword)** search type.

   > **Note**: Some users are finding newly created indexes unavailable right away. Refreshing the browser usually helps, but if you're still experiencing the issue where it can't find the index you may need to wait until the index is recognized.

1. After the index has been added and the chat session has restarted, resubmit the prompt `Where can I stay in New York?`
1. Review the response, which should be based on data in the index.

## Use the index in a prompt flow

Your vector index has been saved in your Azure AI Foundry project, enabling you to use it easily in a prompt flow.

1. In Azure AI Foundry portal, in your project, in the navigation pane on the left, under **Build and customize**, select the **Prompt flow** page.
1. Create a new prompt flow by cloning the **Multi-Round Q&A on Your Data** sample in the gallery. Save your clone of this sample in a folder named `brochure-flow`.
    <details>  
      <summary><b>Troubleshooting tip</b>: Permissions error</summary>
        <p>If you receive a permissions error when you create a new prompt flow, try the following to troubleshoot:</p>
        <ul>
          <li>In the Azure portal, in the resource group for your Azure AI Foundry hub, select the AI Services resource.</li>
          <li>Under <b>Resource Management</b>, in the <b>Identity</b> tab, ensure that the status of <b>System assigned</b>> managed identity is <b>On</b>.</li>
          <li>In the resource group for your Azure AI Foundry hub, select the Storage Account</li>
          <li>On the <b>Access control (IAM)</b> page, add a role assignment to assign the <b>Storage blob data reader</b> role to the managed Identity for your Azure AI services resource.</li>
          <li>Wiat for the role to be assigned, and then retry the previous step.</li>
        </ul>
    </details>

1. When the prompt flow designer page opens, review **brochure-flow**. Its graph should resemble the following image:

    ![A screenshot of a prompt flow graph.](./media/chat-flow.png)

    The sample prompt flow you are using implements the prompt logic for a chat application in which the user can iteratively submit text input to chat interface. The conversational history is retained and included in the context for each iteration. The prompt flow orchestrate a sequence of *tools* to:

    - Append the history to the chat input to define a prompt in the form of a contextualized form of a question.
    - Retrieve the context using your index and a query type of your own choice based on the question.
    - Generate prompt context by using the retrieved data from the index to augment the question.
    - Create prompt variants by adding a system message and structuring the chat history.
    - Submit the prompt to a language model to generate a natural language response.

1. Use the **Start compute session** button to start the runtime compute for the flow.

    Wait for the compute session to start. This provides a compute context for the prompt flow. While you're waiting, in the **Flow** tab, review the sections for the tools in the flow.

    Then, when the compute session has started...

1. In the **Inputs** section, ensure the inputs include:
    - **chat_history**
    - **chat_input**

    The default chat history in this sample includes some conversation about AI.

1. In the **Outputs** section, ensure that the output includes:

    - **chat_output** with value ${chat_with_context.output}

1. In the **modify_query_with_history** section, select the following settings (leaving others as they are):

    - **Connection**: *The default Azure OpenAI resource for your AI hub*
    - **Api**: chat
    - **deployment_name**: gpt-4
    - **response_format**: {"type":"text"}

1. Wait for the compute session to start, then in the **lookup** section, set the following parameter values:

    - **mlindex_content**: *Select the empty field to open the Generate pane*
        - **index_type**: Registered Index
        - **mlindex_asset_id**: brochures-index:1
    - **queries**: ${modify_query_with_history.output}
    - **query_type**: Hybrid (vector + keyword)
    - **top_k**: 2

1. In the **generate_prompt_context** section, review the Python script and ensure that the **inputs** for this tool include the following parameter:

    - **search_result** *(object)*: ${lookup.output}

1. In the **Prompt_variants** section, review the Python script and ensure that the **inputs** for this tool include the following parameters:

    - **contexts** *(string)*: ${generate_prompt_context.output}
    - **chat_history** *(string)*: ${inputs.chat_history}
    - **chat_input** *(string)*: ${inputs.chat_input}

1. In the **chat_with_context** section, select the following settings (leaving others as they are):

    - **Connection**: *The default Azure OpenAI resource for your AI hub*
    - **Api**: Chat
    - **deployment_name**: gpt-4
    - **response_format**: {"type":"text"}

    Then ensure that the **inputs** for this tool include the following parameters:
    - **prompt_text** *(string)*: ${Prompt_variants.output}

1. On the toolbar, use the **Save** button to save the changes you've made to the tools in the prompt flow.
1. On the toolbar, select **Chat**. A chat pane opens with the sample conversation history and the input already filled in based on the sample values. You can ignore these.
1. In the chat pane, replace the default input with the question `Where can I stay in London?` and submit it.
1. Review the response, which should be based on data in the index.
1. Review the outputs for each tool in the flow.
1. In the chat pane, enter the question `What can I do there?`
1. Review the response, which should be based on data in the index and take into account the chat history (so "there" is understood as "in London").
1. Review the outputs for each tool in the flow, noting how each tool in the flow operated on its inputs to prepare a contextualized prompt and get an appropriate response.

    You now have a working prompt flow that uses your Azure AI Search index to implement the RAG pattern. To learn more about how to deploy and consume your prompt flow, see the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/how-to/flow-deploy).

## Create a RAG client app with the Azure AI Foundry and Azure OpenAI SDKs

While a prompt flow is a great way to encapsulate your model and data in a RAG-based application, you can also use the Azure AI Foundry and Azure OpenAI SDKs to implement the RAG pattern in a client application. Let's explore the code to accomplish this in a simple example.

> **Tip**: You can choose to develop your RAG solution using Python or Microsoft C#. Follow the instructions in the appropriate section for your chosen language.

### Prepare the application configuration

1. In the Azure AI Foundry portal, view the **Overview** page for your project.
1. In the **Project details** area, note the **Project connection string**. You'll use this connection string to connect to your project in a client application.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab). Then in the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.
1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal.

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the cloud shell toolbar, in the **Settings** menu, select **Go to Classic version** (this is required to use the code editor).

    > **Tip**: As you paste commands into the cloudshell, the ouput may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. In the PowerShell pane, enter the following commands to clone the GitHub repo for this exercise:

    ```
    rm -r mslearn-ai-foundry -f
    git clone https://github.com/microsoftlearning/mslearn-ai-studio mslearn-ai-foundry
    ```

> **Note**: Follow the steps for your chosen programming language.

1. After the repo has been cloned, navigate to the folder containing the chat application code files:  

    **Python**

    ```
   cd mslearn-ai-foundry/labfiles/rag-app/python
    ```

    **C#**

    ```
   cd mslearn-ai-foundry/labfiles/rag-app/c-sharp
    ```

1. In the cloud shell command line pane, enter the following command to install the libraries you'll use:

    **Python**

    ```
   pip install python-dotenv azure-ai-projects azure-identity openai
    ```

    **C#**

    ```
   dotnet add package Azure.Identity
   dotnet add package Azure.AI.Projects --prerelease
   dotnet add package Azure.AI.OpenAI --prerelease
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
    - **your_project_endpoint**: Replace with the connection string for your project (copied from the project **Overview** page in the Azure AI Foundry portal)
    - **your_model_deployment** Replace with the name you assigned to your model deployment (which should be `gpt-4`)
    - **your_index**: Replace with your index name (which should be `brochures-index`)
1. After you've replaced the placeholders, use the **CTRL+S** command to save your changes and then use the **CTRL+Q** command to close the code editor while keeping the cloud shell command line open.

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
    - Uses the Azure AI Foundry SDK to connect to your project (using the project connection string)
    - Retrieves the default Azure AI Search connection from your project so it can determine the endpoint and key for your Azure AI Search service.
    - Creates an authenticated Azure OpenAI client based on the default Azure OpenAI service connection in your project.
    - Submits a prompt (including a system and user message) to the Azure OpenAI client, adding additional information about the Azure AI Search index to be used to ground the prompt.
    - Displays the response from the grounded prompt.
1. Use the **CTRL+Q** command to close the code editor without saving any changes, while keeping the cloud shell command line open.

### Run the chat application

1. In the cloud shell command line pane, enter the following command to run the app:

    **Python**

    ```
   python rag-app.py
    ```

    **C#**

    ```
   dotnet run
    ```

1. When prompted, enter a question, such as `Where can I travel to?` and review the response from your generative AI model.

    Note that the response includes source references to indicate the indexed data in which the answer was found.

1. Try a few more questions, for example `Where should I stay in London?`

    > **Note**: This simple example application doesn't include any logic to retain the conversation history, so each prompt is treated as a new conversation.

1. When you're finished, enter `quit` to exit the program. Then close the cloud shell pane.

## Challenge

Now you've experienced how to integrate your own data in a generative AI app built with the Azure AI Foundry portal, let's explore further!

Try adding a new data source through the Azure AI Foundry portal, index it, and integrate the indexed data in a prompt flow. Some data sets you could try are:

- A collection of (research) articles you have on your computer.
- A set of presentations from past conferences.
- Any of the datasets available in the [Azure Search sample data](https://github.com/Azure-Samples/azure-search-sample-data) repository.

Be as resourceful as you can to create your data source and integrate it in a prompt flow or client app. Test your solution by submitting prompts that could only be answered by the data set you chose!

## Clean up

To avoid unnecessary Azure costs and resource utilization, you should remove the resources you deployed in this exercise.

1. If you've finished exploring Azure AI Foundry, return to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and sign in using your Azure credentials if necessary. Then delete the resources in the resource group where you provisioned your Azure AI Search and Azure AI resources.
