---
lab:
    title: 'Create a RAG-based copilot'
---

# Create a RAG-based copilot

Retrieval Augmented Generation (RAG) is a technique used to build applications that integrate data from custom data sources into a prompt for a generative AI model. RAG is a commonly used pattern for developing custom *copilots* - chat-based applications that use a language model to interpret inputs and generate appropriate responses.

In this exercise, you'll use Azure AI Studio to integrate custom data into a generative AI prompt flow.

> **Note**: Azure AI Studio is in preview at the time of writing, and is under active development. Some elements of the service may not be exactly as-described, and some features may not work as expected.

This exercise takes approximately **45** minutes.

## Create an Azure AI Search resource

Your copilot solution will integrate custom data into a prompt flow. To support this integration, you'll need an Azure AI Search resource with which to index your data.

1. In a web browser, open the [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and sign in using your Azure credentials.
1. On the home page, select **+ Create a resource** and search for `Azure AI Search`. Then create a new Azure AI Search resource with the following settings:
    - **Subscription**: *Select your Azure subscription*
    - **Resource group**: *Select or create a resource group*
    - **Service name**: *Enter a unique service name*
    - **Location**: *Select any available location*
    - **Pricing tier**: Standard
1. Wait for your Azure AI Search resource deployment to be completed.

## Create an Azure AI project

Now you're ready to create an Azure AI Studio project and the Azure AI resources to support it.

1. In a web browser, open [https://ai.azure.com](https://ai.azure.com) and sign in using your Azure credentials.
1. on the **Build** page, select **+ New project**. Then, in the **Create a new project** wizard, create a project with the following settings:
    - **Project name**: *A unique name for your project*
    - **Azure AI resource**: *Create a new resource with the following settings:*
        - **Resource name**: *A unique name*
        - **Subscription**: *Your Azure subscription*
        - **Resource group**: *Select the resource group containing your Azure Ai Search resource*
        - **Location**: *The same location as your Azure AI Search resource (or a location geographically near it)*
        - **Advanced options**:
            - **AI Services provider**: New multi-service provider
            - **Azure AI Search**: *Select your Azure AI Search resource*
1. Select **Next**. Select **Create a project**. Wait for your project to be created.

## Add data to your project

The data for your copilot consists of a set of travel brochures in PDF format from the fictitious travel agency *Margie's Travel*. Let's add them to the project.

1. Download the zipped archive of brochures from [https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip] and extract it to a folder named **brochures** on your local file system.
1. In Azure AI Studio, in your project, in the navigation pane on the left, under **Components**, select the **Data** page.
1. Select **+ New data** and add a new data source connection by uploading the **brochures** folder. Name the new data source **brochures**.

## Create an index for your data

Now that you've added a data source to your project, you can use it to create an index in your Azure Ai Search resource.

1. In Azure AI Studio, in your project, in the navigation pane on the left, under **Components**, select the **Indexes** page.
1. Add  a new index with the following settings:
    - **Source data**:
        - **Data source**: Use existing project data
            - *Select the **brochures** data source*
    - **Index storage**:
        - *Connect to the Azure Ai Search resource in your subscription*
    - **Search settings**:
        - **Search type**: Vector
        - **Azure OpenAI Resource**: Default_AzureOpenAI
        - *Acknowledge that an embedding model will be deployed*
    - **Index settings**:
        - **Index name**: brochures-index
        - **Virtual machine**: Auto select
1. Wait for your index to be created, which can take several minutes. The index creation operation consists of the following jobs:
    - Validating deployment of the embedding model that will be used to create embedding vectors for your data
    - Chunking the text data into smaller units for indexing
    - Creating embeddings for the text tokens in your chunked data
    - Creating the index
    - Registering the index asset
    - Creating a prompt flow that uses the index

## Deploy a model and test the index

Before using your index in a RAG-based prompt flow, let's deploy a model and verify that it can be used to affect generative AI responses.

1. In Azure AI Studio, in your project, in the navigation pane on the left, under **Components**, select the **Deployments** page.
1. Create a new deployment of the **gpt-35-turbo** model with an appropriate name. Set the **Advanced** options to use the default content filter and to restrict the tokens-per-minute (TPM) to **5K**.
1. In the navigation pane on the left, under **Tools**, select the **Playground** page.
1. On the Playground page, in the **AConfiguration** pane, ensure that your gpt-35-turbo model deployment is selected. Then, in the **Chat session** pane, submit the prompt `Where can I stay in New York?`
1. Review the response, which should be a generic answer from the model without any data from the index.
1. In the **Assistant setup** pane, select **Add your data** and then add a data source with the following settings:
    - **Data source**:
        - **Select data source**: Azure AI Search
        - **Subscription**: *Your Azure subscription*
        - **Azure AI Search service**: *Your Azure AI Search resource*
        - **Azure AI Search index**: brochures-index
        - **Add vector search**: <u>un</u>selected
        - *Select the acknowledgement statement*
    - **Data field mapping**:
        - **Content data**: content
        - **File name**: filepath
        - **Title**: title
        - **URL**: url
    - **Data management**:
        - **search type**: keyword
1. After the data source has been added and the chat session has restarted, resubmit the prompt `Where can I stay in New York?`
1. Review the response, which should be based on data in the index.

## Use the index in a prompt flow

When you created the index, a sample prompt flow that uses it was created automatically

1. In Azure AI Studio, in your project, in the navigation pane on the left, under **Tools**, select the **Prompt flow** page.
1. Select the **brochures-index-sample-flow** prompt flow that was created for your index.
1. In the **Runtime** list, select **Start** to start the automatic runtime. Then wait for it to start.
1. Explore and update the tools in the flow:
    - **Inputs** (the text inputs for the flow):
        - Ensure that the inputs include **chat_history** and **question**.
    - **Outputs** (the text outputs from the flow):
        - Ensure that the **output** is set to *${answer_the_question_with_context.output}*
    - **modify_query_with_history** (modifies the prompt to include the chat history (if any) and ask the submitted question):
        - Ensure that the **Connection** is set to *Default_AzureOpenAI*, **deployment_name** is set to your gpt-35-turbo deployment, and set **max_tokens** to 1000.
        - Select **Validate and parse input**.
    - **embed_the_question** (creates a vector embedding for the question text):
        - Ensure that the **Connection** is set to *Default_AzureOpenAI*, **deployment_name** is set to the embeddings deployment, and the **input** is set to to *${modify_query_with_history.output}**
        - Select **Validate and parse input**.
    - **search_question_from_indexed_docs** (searches the index based on the question):
        - Ensure **query** is set to *\${embed_the_question.output}*.
        - Select **Validate and parse input**.
    - **generate_prompt_context** (generates context from search results to be added to the prompt):
        - Ensure **search_result** is set to *\${search_question_from_indexed_docs.output}*.
        - Select **Validate and parse input**.
    - **Prompt_variants** (Adds context to the prompt):
        - Ensure **contexts** is set to *\${generate_prompt_context.output}*, **question** is set to *\${flow.question}*, and **chat_history** is set to *\${flow.chat_history}*.
        - Select **Validate and parse input**.
    - **answer_the_question_with_context** (Uses a generative AI model to answer the question in the contextualized prompt):
        - Ensure that the **Connection** is set to *Default_AzureOpenAI*, **deployment_name** is set to your gpt-35-turbo deployment, and set **max_tokens** to 1000.
        - Select **Validate and parse input**.
1. On the toolbar, select **Chat**.
1. In the chat pane, enter the question `Where can I stay in London?`
1. Review the response, which should be based on data in the index.
1. Review the outputs for each tool in the flow.
1. In the chat pane, enter the question `What can I do there?`
1. Review the response, which should be based on data in the index and take into account the chat history (so "there" is understood as "in London").
1. Review the outputs for each tool in the flow.

## Deploy the flow

Now that you have a working flow that uses your indexed data, you can deploy it as a service to be consumed by a copilot application.

1. On the toolbar, select **Deploy**.
1. Create a deployment with the following settings:
    - **Basic settings**:
        - **Endpoint**: New
        - **Endpoint name**: brochure-flow
        - **Deployment name**: brochure-flow-1
        - **Virtual machine**: Standard_DS3_v2
        - **Instance count**: 1
        - **Inferencing data collection**: Unselected
        - **Application insights diagnostics**: Unselected
    - **Advanced settings**:
        - *Use the default settings*
1. In Azure AI Studio, in your project, in the navigation pane on the left, under **Components**, select the **Deployments** page.
1. Keep refreshing the view until the **brochure-flow-1** deployment is shown as having succeeded under the **brochure-flow** endpoint (this may take some time).
1. When the deployment has succeeded, select it. Then, on its **Test** page, enter the prompt `What is there to do in San Francisco?` and review the response.

**FAILS WITH PERMISSIONS ERROR**
