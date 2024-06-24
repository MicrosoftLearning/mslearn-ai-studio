---
lab:
    title: 'CHALLENGE: Build a custom copilot code-first with the Azure AI Studio'
---

# Build a custom copilot code-first with the Azure AI Studio

In this exercise, you'll clone and deploy an Azure Developer CLI AI project template, and you'll use it as a starting point to build your own custom copilot with Azure AI and a code-first experience.

> To complete this exercise, your Azure subscription must be approved for access to the Azure OpenAI service. Fill in the [registration form](https://learn.microsoft.com/legal/cognitive-services/openai/limited-access) to request access to Azure OpenAI models.
> You'll also need a GitHub account to fork the project repository and test it in a GitHub Codespaces environment. Create a free account [here](https://github.com/).

This exercise will take approximately **90** minutes.

## Clone and deploy an Azure Developer CLI AI project template

To get started with the Azure Developer CLI AI project template, navigate to the [Azure AI Templates with Azure Developer CLI collection](https://learn.microsoft.com/collections/5pq0uompdgje8d/?WT.mc_id=academic-140829-cacaste). By exploring the collection, you can find several projects grouped by technology and use case, including multi-modal and multi-agent projects samples, copilot-like projects and samples integrating different frameworks and Azure services.

For this exercise, you'll take the **[Contoso Chat Retail copilot with Azure AI Studio & PromptFlow (Python)](https://aka.ms/contoso-retail-sample)** project template as an example. This project template is a code-first experience that uses Prompty and PromptFlow to build a custom copilot for a retail chatbot assistant of a fictional company called Contoso Outdoors.  The solution uses a Retrieval Augmented Generation (RAG) pattern to ground responses in the company's product and customer data. Customers can ask questions about the retailer's product catalog, and also get recommendations based on their prior purchases.

By selecting the project link included in the collection, you'll be redirected to the GitHub repository hosting the template code. The [README.md](https://github.com/Azure-Samples/contoso-chat/blob/main/README.md) file in the repository provides a detailed description of the project, including the architecture, the prerequisites, and the steps to deploy the project.

![Contoso Chat Architecture](./media/contoso_chat_architecture.png)

### Set up GitHub Codespaces

In this exercise you'll use [GitHub Codespaces](https://github.com/features/codespaces), a GitHub feature that lets you create a cloud-hosted development environment directly within GitHub. This way, you can quickly start coding without having to set up your local development environment, because the codespaces is pre-configured with the necessary tools and dependencies, specified in the dev container configuration files. To initialize your environment, follow the steps below:

1. **Fork the repository**: Select the **Fork** button in the top right corner of the GitHub repository page to create a copy of the repository in your GitHub account.
1. Once you have your forked repository, select the **Code** button and select **Codespaces**. Then select on the **+** button to create a new codespace on the main branch of your forked repository.

    ![Create GitHub Codespaces](./media/create_codespaces.png)

1. In a few seconds, you'll be redirected to a new browser tab with the Codespaces environment, which comes attached with a Visual Studio Code editor. You can either continue working here or open the environment in your local Visual Studio Code (VS Code) editor by clicking the **Open in VS Code Desktop** button from the top left menu.

### Connect to your Azure subscription

The next step is connecting your local environment with the Azure subscription where you'd like to deploy the project.

1. Install the [Azure Developer CLI](https://aka.ms/install-azd?WT.mc_id=academic-140829-cacaste).
1. Sign in into your Azure Account from the VS Code terminal. Use the following command:

    ```bash
        azd auth login --use-device-code
    ```

### Provision the necessary Azure resources

1. Once you are logged in, you are ready to start provisioning the Azure resources for the project in your subscription. You can do that in the same VS Code terminal you used for login, by running the following command:

    ```bash
        azd up
    ```

1. You will be prompted to enter the **environment name**, the **Cloud location** and the **subscription** where you want to deploy the resources. We recommend using *Sweden Central* as Cloud region, as it is the region where the majority of the Azure OpenAI models are available.

The execution of this command will take a few minutes; at the end of the process, you'll have all the Azure resources deployed and configured for the project within a new resource group in your Azure subscription. Once finalized, you can navigate on the [Azure Portal](https://ms.portal.azure.com/) to explore the newly created resources, including:

* An **Azure AI Studio Hub**, which is a centralized workspace to manage your AI projects and resources in Azure AI Studio.
* An **Azure AI Studio Project**, which is a container for your AI project resources, including datasets, models, and experiments.
* An **Azure AI services resource**, which is a resource that provides access to the Azure AI services, including the Azure OpenAI service.
* An **Application Insights resource**, which is a resource that provides monitoring and telemetry for your AI project.
* A **Cosmos DB account**, which is a database service hosting the customer data for the Contoso Outdoors chatbot, to enable a personalized chat experience.
* A **Container Registry**, which is a private registry to store and manage the Docker images used in the project.
* A **Key Vault**, which is a secure store for your project secrets and keys.
* An **Azure AI Search Service**, which is a service to index and search the product catalog data for the Contoso Outdoors chatbot.
* An **Azure Storage account**, which is a storage service for AI project data management.

### Explore the provisioned assets

You can explore the newly created Azure AI Hub and Project through the [Azure AI Studio](https://ai.azure.com) portal.

1. In the Azure AI Studio, navigate to the **Deployments** page to see the deployed Azure OpenAI service instances, such as:

    * A **gpt-35-turbo model** deployment, that is used as the chat engine.
    * A **gpt-4 model** deployment, that is used for the AI assisted evaluation.
    * A **text-embedding-ada-002 model** deployment, that is used to enable vector search over the product catalog.

    The **azd up** command also creates a **machine learning online endpoint** and deploys the final application to it.

1. In the **Deployments** tab, you can see the deployed endpoint and api key, along with a sample code snippet to consume it from your application, in several languages.
1. You can also test the endpoint directly from the Azure AI Studio portal, by selecting on the **Test** button and entering a sample text to get the response from the deployed model. Try with the following:

    ```bash
            {"question": "tell me about your jackets", "customerId": "3", "chat_history": []}
    ```

1. You can also test the flow locally, by running the following command in the VS Code terminal:

    ```bash
        pf flow test --flow ./contoso_chat --inputs question="tell me about your jackets" customerId="3" chat_history=[]
    ```

    In both cases you should get an output similar to the one below:
    ![Example App Output](./media/example_app_output.png)

## Explore and customize the Contoso Chat Retail copilot sample

Before you start customizing the Contoso Chat Retail copilot, you should familiarize yourself with the project structure and the codebase. The project is organized in the following folders:

* **infra folder**, containing all of the Bicep files for the azd template, executed to create the Azure resources required to host the app.
* **azure.yaml** file, a configuration file defining the provisioning and post-provisioning steps for the Azure resources.
* **.azure folder**, containing essential Azure configurations and environment variables, such as the location to deploy resources or other subscription information.
* **.github folder**, holding the CI/CD workflow files for GitHub Actions and the default CI/CD provider for azd.
* **.devcontainer folder**, including the devcontainer configuration files for the GitHub Codespaces environment.
* **contoso-chat folder**, containing all of the deployable app source code. This is where you will mostly work to customize the copilot. In particular, the contoso-chat folder contains:
    * A **chat.prompty** file, which includes the system message specification, some safety guardrails, and the placeholders for the relevant context retrieved from the product catalog index and the customer data.
    * A **flow.flex.yaml** file, which contains the description of the input and the entry point for the flex flow - the Python function 'get _response'.
    * A **chat_request.py** script, containing the definition of the 'get_response' function. This entry point function performs several actions:
        * It retrieves the customer information and the history of products purchases through the customer Id , by looking into the Cosmos DB.
        * It gets the information about the product catalog relevant to the user query by searching the Azure AI Search Service.
        * It loads the prompty file, fills in all the dynamic fields with the info retrieved - customer order history and product catalog context - to build the final prompt, which is then used to execute the prompty, which means calling the LLM and getting a final response.

### Buid your own custom copilot

To build your own custom copilot, there's a few steps you can follow:

1. **Replace the fictious customer data**: You can replace the fictious customer data in the Cosmos DB with your own data, through the Azure Portal or the Azure CLI. You can also modify the Cosmos DB schema to fit with your data structure.
1. **Replace the product catalog data**: You can replace the product catalog data in the Azure AI Search Service with your own data, through the Azure Portal or the Azure CLI. You can also modify the Azure AI Search Service schema to fit with your data structure.
1. **Customize the chat.prompty file**: You can modify the system message specification and the safety guardrails to align with your own use-case. You can also edit the placeholders for the relevant context retrieved from the product catalog index and the customer data, to fit with the data you have in your Cosmos DB and Azure AI Search Service.

### Test your custom copilot locally

1. To test your customized application locally, you can run the following command in the VS Code terminal:

    ```bash
        pf flow test --flow <flow-path> --inputs question=<your-question> customerId=<customer_id> chat_history=<chat-history>
    ```

1. To deploy the new version of the application to the Azure subscription, you can run the following command:

    ```bash
        azd deploy
    ```

1. In addition to that, you should also replace the test dataset used to run the app evaluation pipeline through GitHub Actions with your own data. The test dataset is located in the **data** folder of the project, and it is in a .jsonl format. You can replace the file with your own data, and then run the evaluation pipeline by pushing the changes to the main branch of your forked repository. The evaluation pipeline will run automatically, and you can check the results in the GitHub Actions tab of your repository.
1. You can even customize the evaluation pipeline by modifying the *evaluate.yaml* file in the *.github/workflows* folder of the project and the *evaluations_chat.py* script in the *evaluations* folder.

## Delete Azure resources

When you finish exploring the Azd CLI sample project, you should delete the resources you’ve created to avoid unnecessary Azure costs. You can do this by running the following command in the VS Code terminal:

```bash
    azd down
```
