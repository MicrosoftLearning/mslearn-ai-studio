---
lab:
    title: 'CHALLENGE: Build a custom copilot code-first with the Azure AI Studio'
---

# Build a custom copilot code-first with the Azure AI Studio

In this exercise, you'll clone and deploy an Azure Developer CLI template that provisions and [deploys your AI project to an ML online endpoint](https://learn.microsoft.com/azure/developer/azure-developer-cli/azure-ai-ml-endpoints) on Azure AI Studio. You'll then use it as a starting point to build your own custom copilot with Azure AI and a code-first experience. 

> To complete this exercise, your Azure subscription must be approved for access to the Azure OpenAI service. Fill in the [registration form](https://learn.microsoft.com/legal/cognitive-services/openai/limited-access) to request access to Azure OpenAI models.
> You'll also need a GitHub account to fork the project repository and test it in a GitHub Codespaces environment. Create a free account [here](https://github.com/). You'll need the Basic Tier of Azure AI Search to activate Semantic Ranker. Learn about pricing [here](https://azure.microsoft.com/pricing/details/search/). You'll also need to deploy three OpenAI models (`gpt-35-turbo`, `gpt-4`, `text-embedding-ada-002`). Learn about model region availability [here](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability).

This exercise will take approximately **90** minutes.

## Clone and deploy an Azure Developer CLI AI project template

To get started with the Azure Developer CLI AI project template, navigate to the [Azure AI Templates with Azure Developer CLI collection](https://learn.microsoft.com/collections/5pq0uompdgje8d/?WT.mc_id=academic-140829-cacaste). By exploring the collection, you can find several projects grouped by technology and use case, including multi-modal and multi-agent projects samples, copilot-like projects and samples integrating different frameworks and Azure services.

For this exercise, you'll take the **[Contoso Chat Retail copilot with Azure AI Studio & PromptFlow (Python)](https://aka.ms/contoso-retail-sample)** project template as your starting point. This project template is a code-first experience that uses Prompty and PromptFlow to build a custom copilot (chat AI) that can be integrated into the retail  website (chat UI) of a fictional company called Contoso Outdoors, as shown below. 

![Contoso Chat UI/UX](./media/contoso_outdoors_website.png)

The retail copilot solution uses a Retrieval Augmented Generation (RAG) pattern to ground responses in the company's product and customer data. Customers can ask the retail chatbot questions about the company's product catalog, and also get recommendations based on their prior purchases.

By selecting the project link included in the collection, you'll be redirected to the GitHub repository hosting the template code. The [README.md](https://github.com/Azure-Samples/contoso-chat/blob/main/README.md) file in the repository provides a detailed description of the project, including the architecture, the prerequisites, and the steps to deploy the project.

![Contoso Chat Architecture](./media/contoso_chat_architecture.png)

### 1. Set up GitHub Codespaces

In this exercise you'll use [GitHub Codespaces](https://github.com/features/codespaces), a GitHub feature that lets you launch a pre-configured cloud-hosted [development container](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers) directly from your repository, with one click. This way, you can quickly start coding without having to set up your local development environment, since the Codespaces already has all necessary tools and dependencies pre-installed. 

To initialize your development environment, follow the steps below:

1. **Fork the repository**: Select the **Fork** button in the top right corner of the GitHub repository page to create a copy of the repository in your GitHub account.
1. Once you have your forked repository, select the **Code** button and select **Codespaces**. Then select on the **+** button to create a new codespace on the main branch of your forked repository.

    ![Create GitHub Codespaces](./media/create_codespaces.png)

1. In a few seconds, you'll be redirected to a new browser tab where the Codespaces environment is setup with an [attached Visual Studio Code editor](https://code.visualstudio.com/docs/devcontainers/containers) by default. You can either continue working in the browser tab, or reconnect to the running Codespaces from your local Visual Studio Code editor by clicking the **Open in VS Code Desktop** button from the top left menu.

### 2. Connect VS Code environment to Azure

The next step is connecting your local development environment with the Azure subscription where you'd like to deploy the project. Start by opening a new terminal in your Visual Studio Code IDE.

1. First, verify that the [latest version](https://github.com/Azure/azure-dev/releases/tag/azure-dev-cli_1.9.3) of Azure Developer CLI is installed.
    ```bash
        azd version
    ```

1. Next, sign in into your Azure Account from the VS Code terminal.

    ```bash
        azd auth login 
    ```

### 3. Provision Azure resources for your project

Once you are logged in, you are ready to start provisioning the Azure resources for the project in your subscription. You can do that in the same VS Code terminal you used for login.

1. Provision _and deploy_ your AI application using azd.

    ```bash
        azd up
    ```

1. You should see the following prompts. Respond using the guidance below:
    - _Enter a new environment name:_ - this will decide your resource group name.
    - _Select an Azure Subscription to use_ - this should be pre-approved for Azure Open AI.
    - _Select an Azure location to use_ - pick a location with model quota available.

We recommend using `sweden central` as the Azure location since it is the region where the majority of the Azure OpenAI models are available.

This command can take 10 minutes or more to complete. You can track progress by:
 - _Viewing detailed progress in the [Azure Portal](https://ms.portal.azure.com/)_. Look for the Resource Group corresponding to your environment name. Click the _Deployments_ option in the sidebar, then monitor the deploymen status of the resources being created.
 - _Visiting the [Azure AI Studio](https://ai.azure.com) portal_. Log in using your Azure account. Look for the AI hub corresponding to the resource group above (you may need to refresh a few times). Click the listed AI project, then click _Deployments_ in its sidebar to track status for models & chat app.

### 4. Validate Provisioning: Using Azure Portal

Navigate to the [Azure Portal](https://ms.portal.azure.com/) in the browser. Log in and find the Resource Group corresponding to the subscription and environment name you chose earlier. The _Overview_ panel should look like this:

![Azure Portal Resource Group Overview](./media/azure-portal-resource-group.png)

Let's start by verifying that the key [Azure AI Studio architecture](https://learn.microsoft.com/en-us/azure/ai-studio/concepts/architecture) resources were created. The figure below provides more details on what each of these resources provides to our AI application.

1. **Azure AI hub** - top-level Azure resource. Provides a collaboration environment for teams.
1. **Azure AI project** - child of hub. Groups app components for orchestration, customization.
1. **Azure AI services** - managing your model endpoints, integrating other cognitive services.

![Azure AI Studio Architecture](https://learn.microsoft.com/en-us/azure/ai-studio/media/concepts/resource-provider-connected-resources.svg)

Next, let's verify that we provisioned two key resources for implementing our [Retrieval-Augmented Generation](https://learn.microsoft.com/azure/ai-studio/concepts/retrieval-augmented-generation) design pattern by storing the product and customer data for query-driven retrieval.

1. **Search service** - to manage search indexes for our product catalog data.
1. **Azure Cosmos DB account** - to create a database for our customer order data.

Next, we can validate that we have support resources for managing our application LLM ops needs:
1. **Application Insights** - to support monitoring and telemerty for the deployed application.
1. **Container Registry** - to store and manage Docker images used in the project, privately.
1. **Key vault** - to store project secrets (keys, credentials) securely.
1. **Storage account** - to store data related to AI project management (including logs).
1. **Smart detector alert rule** - Application Insights anomaly detector (for requests).

Last but not least, we see a new resource with Type **Machine learning online deployment**. This is the resource corresponding to our deployed Azure AI project endpoint (for the chat copilot).

### 5. Validate Deployment: Using Azure AI Studio

The Azure Portal helps you manage the underlying Azure resources for your project. The Azure AI Studio portal helps you _build and manage_ the AI projects themselves, end-to-end, from model selection to application deployment. The `azd up` command should have completed the entire process from provisioning required models, to deploying & hosting the copilot API endpoint for usage. Let's validate that the application is functioning as expected:
1. Visit the _Manage_ page [Azure AI Studio](https://ai.azure.com/manage) to view all Azure AI hubs in your subscription. 
1. Select the hub for your Resource Group to view all Azure AI projects within it.
1. Select the default AI project in hub, then select _Deployments_ in sidebar.

You should see something like this under the _Model deployments_ tab:
1. Verify that you have an "AzureOpenAI Connection" with:
    - `gpt-35-turbo` - used for chat completion, forming the core chat engine.
    - `gpt-2` - used for chat evaluation, specifically AI-assisted flows.
    - `text-embedding-ada-002` - used for query vectorization & search.
1. Verify that you have an Machine Learning Online "Endpoint" with:
    - `chat-model` - chat AI deployment with `mloe-xxx` endpoint resource.

![Azure AI Project Deployments](./media/azure-ai-project-deployment.png)


### 6. Test Deployment: Using Azure AI Studio (Cloud)

To validate that the deployed copilot works, use the built-in test playground capability, which looks something like this:

![Chat Deployment Details](./media/chat-deployment-details.png)

To get to this page, simply click on the _chat-deployment-xxxx_ resource from the previous step to get this _Details_ page. Then select the "Test" tab to get the test interface shown below. Note that the Details tab also has `Target URI` and `Key` values that you can use with other front-end applications (e.g., Contoso Outdoor website) to integrate this chat assistant for real-world user interactions. For now, test the copilot deployment with a test Input like this:

```bash
  {"question": "tell me about your jackets", "customerId": "3", "chat_history": []}
```

You should get a valid JSON response in the output component as shown below.

![Chat Deployment Test](./media/chat-deployment-test.png)


### 7. Test Deployment: Using Visual Studio Code (Local)

The `azd up` command not only provisions and deploys the application to Azure, it also _configures your local environment_ in Visual Studio Code to support local development, testing, and iteration. Let's check this out.

1. First, validate that your VS Code environment was setup correctly. Look for a `config.json` file in the root folder and check that it has the three properties defined below, with valid values.

    ```json 
    {
        "subscription_id": "xxxxxxxxxxxxxxxx",
        "resource_group": "rg-xxxxxx",
        "workspace_name": "ai-project-xxxxxxx"
    }

    ```
1. Next, check that a `.env` file was created in your root folder. It should contain a list of environment variables _with values filled in_. _The exact variable names may evolve over time._

    ```bash
    AZUREAI_HUB_NAME=
    AZUREAI_PROJECT_NAME=
    AZURE_CONTAINER_REGISTRY_ENDPOINT=
    AZURE_CONTAINER_REGISTRY_NAME=
    AZURE_COSMOS_NAME=
    AZURE_ENV_NAME=
    AZURE_KEY_VAULT_ENDPOINT=
    AZURE_KEY_VAULT_NAME=
    AZURE_LOCATION=
    AZURE_OPENAI_API_VERSION=
    AZURE_OPENAI_CHAT_DEPLOYMENT=
    AZURE_OPENAI_ENDPOINT=
    AZURE_OPENAI_NAME=
    AZURE_RESOURCE_GROUP=
    AZURE_SEARCH_ENDPOINT=
    AZURE_SEARCH_NAME=
    AZURE_SUBSCRIPTION_ID=
    AZURE_TENANT_ID=
    COSMOS_ENDPOINT=
    ```

3. Next, verify that you have the _Promptflow tools_ installed in your development environment.

    ```bash
        pf version
    ```

4. Now, use the `pf flow test` tool to test the _contoso_chat_ flex flow application locally, with the same question we used above. Note the syntax of the command for passing the inputs:

    ```bash
        pf flow test --flow ./contoso_chat --inputs question="tell me about your jackets" customerId="3" chat_history=[]
    ```

You should see a response like this:

![Example App Output](./media/example_app_output.png)


### 8. View Traces: Using Visual Studio Code (Local)

You can trace the details of your execution with the `--ui` flag as shown below. 

    ```bash
        pf flow test --flow ./contoso_chat --inputs question="tell me about your jackets" customerId="3" chat_history=[] --ui
    ```
This should launch a _trace view_ in your browser (in a new tab) with a table that provides high-level details about that test run including the latency and tokens usage.

![pf test row](./media/pf-flow-test-row.png)

Clicking the record expands into a more detail trace view that lets you inspect the finer details of the flow - from the raw data (input, output) to the individual steps of the flow and the relevant components (e.g., prompt templates used for LLM).

![pf test detail](./media/pf-flow-test-detail.png)

### 9. Understand the Contoso Chat Codebase

Your Azure backend is provisioned and ready. Your local development environment is setup and configured to work with your Azure backend. Now, all you need to do is start modifying the contents to customize and redeploy your own version of the application. Let's take a quick look at how the codebase is structured. 

This is a **simplified listing** of the repository, eliminating some files and folders for clarity.

```bash    
data/
    customer_info/  
        create-cosmos-db.ipynb      # Run notebook to upload data to Cosmos DB
        customer_info_1.json        # Example Customer info and orders file
        customer_info_2.json 
        ...
        ...
    product_info/   
        create-azure-search.ipynb   # Run notebook to index product data in AI Search
        products.csv                # Example Products data file

contoso_chat/                       # Main folder for application content
    ai_search.py                    # Search retrieval tool (for RAG design)
    chat.json                       # Example chat file (for Prompty template)
    chat.prompty                    # Chat asset (using Prompty format)
    chat_request.py                 # LLM request tool (for chat completion)
    flow.flex.yaml                  # Promptflow flex flow (define entry point)
    requirements.txt                # App dependencies (define runtime environment)

azure.yaml                          # Main configuration file for Azure Developer CLI  
infra/      
    ai.yaml                         # Define AI model deployments
    app/                            # Infrastructure-as-code config specific to app
    core/                           # Infrastructure-as-code config for core resources
    hooks/                          # Contains post-provisioning scripts
    main.bicep                      # Entry point for Bicep template used by azd
deployment/                         # ai.endpoint config files (named in azure.yaml)
    chat-deployment.yaml 
    chat-model.yaml  
    environment.yaml  

requirements.txt
```

- If you make app changes (in `contoso_chat/`) simply run `azd deploy` to redeploy the application to the previously provisioned backend. No additional re-provisioning or manual intervention steps required. 
- If you make resource changes (in `infra/` folder) then run `azd up` to reprovision and redeploy the application. It should automtically pick up your prior configuration values from `.azure/` and modify them.


### 10. Customize & Redeploy the Copilot

It's time to build your own custom copilot. Here are some things you can explore, to try this out:

1. **Customize the Customer & Order History Data**: 
    - Look at the sample data under `data/customer_info` for a sense of the default schema. 
    - Explore the `data/create-cosmos-db.ipynb` notebook for a code-first approach to data updates.
    - Modify the sample data and run the notebook to change the default Azure CosmosDB database.
    - _Redeploy the app. Try a test question to validate that new customer data is returned_,
1. **Customize the Product Catalog Data**: 
    - Look at the sample data under `data/product_info/` for a sense of the default schema. 
    - Explore the `create-azure-search.ipynb` notebook for a code-first approach to index updates.
    - Modify the sample data and run the notebook to change the default Azure AI Search indexes.
    - _Redeploy the app. Try a test question to validate that new product data is returned_,
1. **Customize the Prompt Template**: 
    - Look at the `contoso_chat/chat.prompty` file for a sense of the default prompt template
    - Look at the `contoso_chat/chat.json` to understand the sample data schema for testing
    - Modify the template (system message, safety, documentation or instructions)
    - Modify the example data if needed
    - _Use the Promptflow CLI to test the flow locally with the new prompt template_
    - _Install and use the Prompty extension to create a new prompt template from scratch_.

Remember:

 - Use `azd deploy` to redeploy your application if you changed only the app code.
 - Use `azd up` to re-provision and re-deploy application if you changed resource configuration.

### 11. Explore Evaluation & Pipeline Automation

1. In addition to that, you should also replace the test dataset used to run the app evaluation pipeline through GitHub Actions with your own data. The test dataset is located in the **data** folder of the project, and it is in a .jsonl format. You can replace the file with your own data, and then run the evaluation pipeline by pushing the changes to the main branch of your forked repository. The evaluation pipeline will run automatically, and you can check the results in the GitHub Actions tab of your repository.
1. You can even customize the evaluation pipeline by modifying the *evaluate.yaml* file in the *.github/workflows* folder of the project and the *evaluations_chat.py* script in the *evaluations* folder.

## Clean Up: Delete Azure resources

This project uses models and services (e.g., Azure AI Search) that can incur non-trivial costs if left running long-term. When you finish exploring this Azure AI AZD template, you should delete the resources you’ve created to avoid unnecessary Azure costs. You can do this by running the following command in the VS Code terminal:

```bash
    azd down
```

This not only reverses the steps taken to provision and deploy the application, it also takes additional steps to _purge_ resources that may otherwise be held in "soft delete" state, impacting your ability to reuse resource names or reclaim model quota. _This command will prompt you about these actions during the shutdown - so make sure you respond correctly_.