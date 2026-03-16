---
lab:
  title: Create a generative AI app that uses your own data
  description: Learn how to use the Retrieval Augmented Generation (RAG) pattern with the Responses API and file search to build a chat app that grounds prompts using your own data.
  level: 300
  duration: 45
  islab: true
---

# Create a generative AI app that uses your own data

Retrieval Augmented Generation (RAG) is a technique used to build applications that integrate data from custom data sources into a prompt for a generative AI model. RAG is a commonly used pattern for developing generative AI apps - chat-based applications that use a language model to interpret inputs and generate appropriate responses.

In this exercise, you'll use the Microsoft Foundry portal and the Responses API to integrate custom data into a generative AI solution. You'll start by experimenting with prompt engineering in the playground, then add grounding data, and finally build a client app that uses the file search tool to ground responses in your own documents.

This exercise takes approximately **45** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

To complete this exercise, you need:

- An [Azure subscription](https://azure.microsoft.com/free/) with permissions to create AI resources.
- [Visual Studio Code](https://code.visualstudio.com/) installed on your local machine.
- [Python 3.13](https://www.python.org/downloads/) or later installed on your local machine.
- [Git](https://git-scm.com/downloads) installed on your local machine.

# Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: Select any of the **AI Foundry recommended** regions

1. Select **Create**. Wait for your project to be created.

## Deploy a model

Now deploy a model that you'll use in your chat application.

1. On the project home page, in the **Start building** menu, select **Browse models**.
1. In the model catalog, search for `gpt-4.1`.
1. Review the model card, and then deploy it using the default settings.
1. When the model has been deployed, it will open in the model playground.

## Use prompt engineering in the playground

Before adding grounding data, let's explore how the model responds using prompt engineering alone. This will help you understand why grounding data matters.

1. After deploying your model, you should be in the playground with that model selected. If not, select **Build** in the top menu bar, then select **Models** on the left, and then select the model you deployed.
1. In the model playground, ensure that your **gpt-4.1** model is selected.
1. In the chat pane, enter the query `Where can I stay in New York?` and review the response.

    The response should be fairly generic — the model provides general knowledge but doesn't have specific information about your travel services.

1. In the **System message** field, enter the following prompt:

    ```
   You are a travel assistant that provides information on travel services available from Margie's Travel.
    ```

1. In the chat pane, enter the same query `Where can I stay in New York?` and review the response.

    The response may be slightly more focused, but the model still doesn't have real data about Margie's Travel offerings. It may even fabricate information. This demonstrates the limitation of prompt engineering alone — while it can guide the model's tone and behavior, it can't provide factual grounding without real data.

1. Try another query: `What destinations does Margie's Travel offer?` and observe how the model responds without grounding data.

## Add grounding data in the playground

Now that you've seen the limitations of prompt engineering alone, let's add real data to ground the model's responses using the RAG pattern.

The data for your app consists of a set of travel brochures in PDF format from the fictitious travel agency *Margie's Travel*.

1. In a new browser tab, download the [zipped archive of brochures](https://microsoftlearning.github.io/mslearn-ai-studio/data/brochures.zip) from `https://microsoftlearning.github.io/mslearn-ai-studio/data/brochures.zip` and extract it to a folder named **brochures** on your local file system.
1. Return to the model playground in the Foundry portal.
1. In the **Tools** section, under the model list, select **Upload files**.
1. Upload the brochure PDF files you extracted earlier. The file search tool allows the model to reference the uploaded documents when answering questions.

    > **Tip**: If you don't see the **Tools** section, ensure you're in the single-model playground view (not comparison mode).

1. After the files have been uploaded, resubmit the prompt `Where can I stay in New York?`
1. Review the response, which should now be based on information from the uploaded brochures — a significant improvement over the prompt engineering-only approach.
1. Try the follow-up question: `What destinations does Margie's Travel offer?` and compare the response to what you got earlier without grounding data.

## Create a RAG client app

Now that you've seen how grounding data works in the playground, let's build a client application that uses the Responses API with the file search tool to implement the RAG pattern programmatically.

### Get the endpoint and key

You'll need an endpoint and key to connect to the model from a client application. In this exercise, we're going to use the OpenAI SDK to chat with the model; and we'll use the Azure OpenAI endpoint to connect to it.

1. On the menu bar, select the **Home** page.
1. Note the **Project API key** and **Azure OpenAI Endpoint** displayed there.

### Get the application files from GitHub

The initial application files you'll need to develop your chat application are provided in a GitHub repo.

1. Open Visual Studio Code.
1. Open the command palette (*Ctrl+Shift+P*) and use the `Git:clone` command to clone the `https://github.com/microsoftlearning/mslearn-ai-studio` repo to a local folder (it doesn't matter which one). Then open it.

    You may be prompted to confirm you trust the authors.

### Prepare the application configuration

1. In Visual Studio Code, view the **Extensions** pane; and if it is not already installed, install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter`. Then select an existing environment if you have one, or create a new **Venv** environment based on your Python 3.1x installation.

    > **Tip**: If you are prompted to install dependencies, you can install the ones in the *requirements.txt* file in the */labfiles/foundry-rag/python/rag-app* folder; but it's OK if you don't - we'll install them later!

1. In the Explorer pane, navigate to the folder containing the application code files at **/labfiles/foundry-rag/python/rag-app**. The application files include:
    - **brochures** (the same folder of brochures you downloaded and extracted previously)
    - **.env** (the application configuration file)
    - **requirements.txt** (the Python package dependencies that need to be installed)
    - **rag-app.py** (the code file for the application)

1. In the **Explorer** pane, right-click the **rag-app** folder containing the application files, and select **Open in integrated terminal** (or open a terminal in the **Terminal** menu and navigate to the */labfiles/foundry-rag/python/rag-app* folder.)

    > **Note**: Opening the terminal in Visual Studio Code will automatically activate the Python environment. You may need to enable running scripts on your system.

1. Ensure that the terminal is open in the **/labfiles/foundry-rag/python/rag-app** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the OpenAI SDK package and other required packages by running the following command:

    ```
    pip install -r requirements.txt openai
    ```

1. In the **Explorer** pane, in the **/labfiles/foundry-rag/python/rag-app** folder, select the **.env** file to open it. Then update the configuration values to include the **Project API key** and **Azure OpenAI Endpoint** for your **gpt-4.1** model.

    > **Tip**: Copy the key and endpoint from the project home page in the Foundry portal, and rename the model deployment if your deployment isn't named *gpt-4.1*

    Save the modified configuration file.

### Write code to implement the RAG pattern

1. In the **Explorer** pane, in the **/labfiles/foundry-rag/python/rag-app** folder, select the **rag-app.py** file to open it.
1. Review the existing code. You will add code to use the OpenAI SDK to access your model.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. At the top of the code file, under the existing namespace references, find the comment **Import namespaces** and add the following code to import the namespace you will need to use the OpenAI SDK:

    ```python
   # import namespaces
   from openai import OpenAI
    ```

1. In the **main** function, note that code to load the endpoint and key from the configuration file has already been provided. Then find the comment **Initialize the OpenAI client**, and add the following code to create a client for the OpenAI API:

    ```python
   # Initialize the OpenAI client
   openai_client = OpenAI(
        base_url=azure_openai_endpoint,
        api_key=api_key
   )
    ```

1. In the **main**function, find the comment **Create vector store and upload files**, and add the following code:

    ```python
   # Create vector store and upload files
   print("Creating vector store and uploading files...")
   vector_store = openai_client.vector_stores.create(
        name="travel-brochures"
   )
   file_streams = [open(f, "rb") for f in glob.glob("brochures/*.pdf")]
   if not file_streams:
        print("No PDF files found in the brochures folder!")
        return
   file_batch = openai_client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
   )
   for f in file_streams:
        f.close()
   print(f"Vector store created with {file_batch.file_counts.completed} files.")
    ```

    This code creates a vector store for your model, and uploads the brochures to it.

1. In the **main** function, note that code to request a user prompt until the user quits the app has been provided. Within this loop, find the **Get a response** comment, and add the following code:

    ```python
   # Get a response
   response = openai_client.responses.create(
        model=model_deployment,
        instructions="You are a travel assistant that provides information on travel services available from Margie's Travel. Only answer questions based on the provided travel brochure data.",
        input=input_text,
        previous_response_id=last_response_id,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store.id]
        }]
   )
   print(response.output_text)
   last_response_id = response.id
    ```

    This code submits a prompt and specifies that the *file_search* tool can be used to search the vector store.

1. Save the changes to the code file. Then, in the terminal pane, use the following command to run the program:

    ```powershell
   python rag-app.py
    ```

    The program should run in the terminal (if not, resolve any errors and try again).

1. When prompted, enter a question, such as `Where should I go on vacation to see architecture?` and review the response from your generative AI model.

    Note that the response should include information grounded in the travel brochure data, with references to the source documents.

1. Try a follow-up question, for example `Where can I stay there?`

1. When you're finished, enter `quit` to exit the program.

## Clean up

If you've finished exploring Microsoft Foundry, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
