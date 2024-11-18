---
lab:
    title: 'Explore the components and tools of the Azure AI Foundry'
---

# Explore the components and tools of the Azure AI Foundry

In this exercise, you use Azure AI Foundry portal to create a project and explore a generative AI model.

This exercise takes approximately **30** minutes.

## Open Azure AI Foundry portal

Let's start by exploring Azure AI Foundry portal.

1. In a web browser, open [https://ai.azure.com](https://ai.azure.com) and sign in using your Azure credentials. The home page of Azure AI Foundry portal looks similar to the following image:

    ![Screenshot of Azure AI Foundry portal.](./media/azure-ai-studio-home.png)

1. Review the information on the home page and view each of the tabs, noting the options to explore models and capabilities, create projects, and manage resources.

## Create an Azure AI hub and project

An Azure AI hub provides a collaborative workspace within which you can define one or more *projects*. Let's create a project and Azure AI hub.

1. In the home page, select **+ Create project**. In the **Create a project** wizard you can see all the Azure resources that will be automatically created with your project, or you can customize the following settings by selecting **Customize** before selecting **Create**:
   
    - **Hub name**: *A unique name*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create a new resource group with a unique name, or select an existing one*
    - **Location**: Select **Help me choose** and then select **gpt-35-turbo** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: *Select to create a new AI Services or use an existing one*
    - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit in scenarios where you are sharing a tenant with other users. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region.

1. If you selected **Customize**, select **Next** and review your configuration.
1. Select **Create** and wait for the process to complete.
   
    After the Azure AI hub and project have been created, it should look similar to the following image:

    ![Screenshot of a Azure AI hub details in Azure AI Foundry portal.](./media/azure-ai-resource.png)

1. Open a new browser tab (leaving the Azure AI Foundry portal tab open) and browse to the Azure portal at [https://portal.azure.com](https://portal.azure.com?azure-portal=true), signing in with your Azure credentials if prompted.
1. Browse to the resource group where you created your Azure AI hub, and view the Azure resources that have been created.

    ![Screenshot of an Azure AI hub and related resources in the Azure portal.](./media/azure-portal.png)

1. Return to the Azure AI Foundry portal browser tab.
1. View each of the pages in the pane on the left side of the page for your Azure AI hub, and note the artifacts you can create and manage. On the **Management center** page, you can select **Connected resources**, either under your hub or your project, and observe that connections to Azure OpenAI and AI services have already been created.
1. If you are in the Management center page, select **Go to project**.

## Deploy and test a model

You can use a project to create complex AI solutions based on generative AI models. A full exploration of all of the development options available in Azure AI Foundry portal is beyond the scope of this exercise, but we'll explore some basic ways in which you can work with models in a project.

1. In the pane on the left for your project, in the **My assets** section, select the **Models + endpoints** page.
1. In the **Models + endpoints** page, in the **Model deployments** tab, select **+ Deploy model**.
1. Search for the **gpt-35-turbo** model from the list, select and confirm.
1. Deploy the model with the following settings by selecting **Customize** in the deployment details:
    - **Deployment name**: *A unique name for your model deployment*
    - **Deployment type**: Standard
    - **Model version**: *Select the default version*
    - **AI resource**: *Select the resource created previously*
    - **Tokens per Minute Rate Limit (thousands)**: 5K
    - **Content filter**: DefaultV2
    - **Enable dynamic quota**: Disabled
      
    > **Note**: Reducing the TPM helps avoid over-using the quota available in the subscription you are using. 5,000 TPM is sufficient for the data used in this exercise.

1. After the model has been deployed, in the deployment overview page, select **Open in playground**.
1. In the **Chat playground** page, ensure that your model deployment is selected in the **Deployment** section.
1. In the chat window, enter a query such as *What is AI?* and view the response:

    ![Screenshot of the playground in Azure AI Foundry portal.](./media/playground.png)

## Clean up

If you've finished exploring Azure AI Foundry portal, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
