---
lab:
    title: 'Create a generative AI app that uses your own data'
    description: 'Learn how to use the Retrieval Augmented Generation (RAG) pattern with the Responses API and file search to build a chat app that grounds prompts using your own data.'
---

# Create a generative AI app that uses your own data

Retrieval Augmented Generation (RAG) is a technique used to build applications that integrate data from custom data sources into a prompt for a generative AI model. RAG is a commonly used pattern for developing generative AI apps - chat-based applications that use a language model to interpret inputs and generate appropriate responses.

In this exercise, you'll use the Microsoft Foundry portal and the Responses API to integrate custom data into a generative AI solution. You'll start by experimenting with prompt engineering in the playground, then add grounding data, and finally build a client app that uses the file search tool to ground responses in your own documents.

This exercise takes approximately **45** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Create a Microsoft Foundry project

Let's start by creating a project and deploying a model.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. Select the project name in the upper-left corner, and then select **Create new project**.
1. Enter a valid name for your project and select **Advanced options** to configure:
    - **Foundry resource**: *Autofilled based on project name* 
    - **Region**: *Select an available region close to you*\*
    - **Subscription**: *Select your subscription*
    - **Resource group**: *Create a new resource group or select an existing one*

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

## Use prompt engineering in the playground

Before adding grounding data, let's explore how the model responds using prompt engineering alone. This will help you understand why grounding data matters.

1. After deploying your model, you should be in the playground with that model selected. If not, select **Build** from the top navigation bar, select **Models** on the left, and then select the model you deployed.
1. In the chat playground, ensure that your **gpt-4.1** model is selected.
1. In the chat window, enter the query `Where can I stay in New York?` and review the response.

    The response should be fairly generic — the model provides general knowledge but doesn't have specific information about your travel services.

1. In the **System message** field, enter the following prompt:

    ```
    You are a travel assistant that provides information on travel services available from Margie's Travel.
    ```

1. Select **Apply changes** to update the system message.
1. In the chat window, enter the same query `Where can I stay in New York?` and review the response.

    The response may be slightly more focused, but the model still doesn't have real data about Margie's Travel offerings. It may even fabricate information. This demonstrates the limitation of prompt engineering alone — while it can guide the model's tone and behavior, it can't provide factual grounding without real data.

1. Try another query: `What destinations does Margie's Travel offer?` and observe how the model responds without grounding data.

## Add grounding data in the playground

Now that you've seen the limitations of prompt engineering alone, let's add real data to ground the model's responses using the RAG pattern.

The data for your app consists of a set of travel brochures in PDF format from the fictitious travel agency *Margie's Travel*.

1. In a new browser tab, download the [zipped archive of brochures](https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip) from `https://github.com/MicrosoftLearning/mslearn-ai-studio/raw/main/data/brochures.zip` and extract it to a folder named **brochures** on your local file system.
1. Return to the chat playground in the Foundry portal.
1. In the **Tools** section of the playground, select **Upload files**.
1. Upload the brochure PDF files you extracted earlier. The file search tool allows the model to reference the uploaded documents when answering questions.

    > **Tip**: If you don't see the Tools section, ensure you're in the single-model playground view (not comparison mode).

1. After the files have been uploaded, resubmit the prompt `Where can I stay in New York?`
1. Review the response, which should now be based on information from the uploaded brochures — a significant improvement over the prompt engineering-only approach.
1. Try the follow-up question: `What destinations does Margie's Travel offer?` and compare the response to what you got earlier without grounding data.

## Create a RAG client app

Now that you've seen how grounding data works in the playground, let's build a client application that uses the Responses API with the file search tool to implement the RAG pattern programmatically.

### Prepare the application configuration

1. In the Microsoft Foundry portal, go to the **Overview** page for your project (the project welcome screen).
1. Find the **Foundry endpoint** displayed on the welcome screen (for example, `https://<your-resource>.services.ai.azure.com/api/projects/<your-project>`). Copy this endpoint — you'll use it to connect to your model.

    > **Note**: The Microsoft Foundry SDK handles authentication and endpoint routing automatically when you use `AIProjectClient.get_openai_client()`. Make a note of this endpoint.

1. Open **Visual Studio Code** on your local computer. If you don't have it installed, download it from [https://code.visualstudio.com](https://code.visualstudio.com).
1. Open a terminal in VS Code (**Terminal > New Terminal**) and clone the GitHub repo containing the code files for this exercise:

    ```
    git clone https://github.com/microsoftlearning/mslearn-ai-studio mslearn-ai-foundry
    ```

1. After the repo has been cloned, open the folder in VS Code (**File > Open Folder**), and navigate to the `mslearn-ai-foundry/labfiles/foundry-rag/python` folder.
1. In the VS Code Explorer pane, review the files in the folder:

    - `.env` - A configuration file for application settings.
    - `rag-app.py` - The Python code file for the RAG application.
    - `requirements.txt` - A file listing the package dependencies.

1. Open a terminal in VS Code and navigate to the project folder, then install the required libraries:

    ```
    cd mslearn-ai-foundry/labfiles/foundry-rag/python
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
1. Copy the **brochures** folder you extracted earlier into the `mslearn-ai-foundry/labfiles/foundry-rag/python` folder. The code will upload these files to create a vector store for file search.

### Write code to implement the RAG pattern

> **Tip**: As you add code, be sure to maintain the correct indentation.

1. In VS Code, open the `rag-app.py` file.
1. In the code file, note the existing statements that have been added at the top of the file to import the necessary packages. Then, find the comment **Add references**, and add the following code to reference the libraries you installed:

    ```python
    # Add references
    import glob
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

1. Find the comment **Upload file and create vector store**, and add the following code to upload the brochure files and create a vector store for file search:

    ```python
    # Upload file and create vector store
    print("Uploading files and creating vector store...")
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

    > **Note**: This code uploads all PDF files from the `brochures` folder, creates a vector store, and waits for the files to be processed. The vector store will be used by the file search tool to find relevant information when answering questions.

1. Note that the code includes a loop to allow a user to input a prompt until they enter "quit", and it tracks conversation state using `previous_response_id`. Find the comment **Get a response** and add the following code to send the user input to your model using the Responses API with the file search tool:

    ```python
    # Get a response
    response = openai_client.responses.create(
        model=model_deployment,
        instructions="You are a travel assistant that provides information on travel services available from Margie's Travel. Only answer questions based on the provided travel brochure data.",
        input=input_text,
        previous_response_id=previous_response_id,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store.id]
        }]
    )
    print(response.output_text)
    previous_response_id = response.id
    ```

    > **Note**: The Responses API uses `previous_response_id` to maintain conversation history automatically. The `file_search` tool is configured with the vector store containing the uploaded brochure data, so the model can search through the documents to find relevant information before responding.

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
    python rag-app.py
    ```

1. When prompted, enter a question, such as `Where should I go on vacation to see architecture?` and review the response from your generative AI model.

    Note that the response should include information grounded in the travel brochure data, with references to the source documents.

1. Try a follow-up question, for example `Where can I stay there?`

1. When you're finished, enter `quit` to exit the program.

> **Tip**: If the app fails because the rate limit is exceeded. Wait a few seconds and try again. If there is insufficient quota available in your subscription, the model may not be able to respond.

## Clean up

If you've finished exploring the Microsoft Foundry portal, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
