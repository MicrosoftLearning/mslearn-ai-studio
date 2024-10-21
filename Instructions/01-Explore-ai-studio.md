---
lab:
    title: 'Explore the components and tools of the Azure AI Studio'
---

# Explore the components and tools of the Azure AI Studio

In this exercise, you use Azure AI Studio to create a project and explore a generative AI model.

This exercise takes approximately **30** minutes.

## Open Azure AI Studio

Let's start by exploring Azure AI Studio.

1. In a web browser, open [https://ai.azure.com](https://ai.azure.com) and sign in using your Azure credentials. The home page of Azure AI Studio looks similar to the following image:

    ![Screenshot of Azure AI Studio.](./media/azure-ai-studio-home.png)

1. Review the information on the home page and view each of the tabs, noting the options to explore models and capabilities, create projects, and manage resources.

## Create an Azure AI hub

You need an Azure AI hub in your Azure subscription to host projects. You can either create this resource while creating a project, or provision it ahead of time (which is what we'll do in this exercise).

1. In the **Management** section, select **All resources**, then select **+ New hub**. Create a new hub with the following settings:
    - **Hub name**: *A unique name*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create a new resource group with a unique name, or select an existing one*
    - **Location**: Select **Help me choose** and then select **gpt-35-turbo** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: *Select to create a new AI Services or use an existing one*
    - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit in scenarios where you are sharing a tenant with other users. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Next** and review your configuration.
1. Select **Create** and wait for the process to complete.
   
    After the Azure AI hub has been created, it should look similar to the following image:

    ![Screenshot of a Azure AI hub details in Azure AI Studio.](./media/azure-ai-resource.png)

1. Open a new browser tab (leaving the Azure AI Studio tab open) and browse to the Azure portal at [https://portal.azure.com](https://portal.azure.com?azure-portal=true), signing in with your Azure credentials if prompted.
1. Browse to the resource group where you created your Azure AI hub, and view the Azure resources that have been created.

    ![Screenshot of an Azure AI hub and related resources in the Azure portal.](./media/azure-portal.png)

1. Return to the Azure AI Studio browser tab.
1. View each of the pages in the pane on the left side of the page for your Azure AI hub, and note the artifacts you can create and manage. On the **Connections** page, observe that connections to Azure OpenAI and AI services have already been created.

## Create a project

An Azure AI hub provides a collaborative workspace within which you can define one or more *projects*. Let's create a project in your Azure AI hub.

1. In Azure AI Studio, ensure you're in the hub you just created (you can verify your location by checking the path at the top of the screen).
1. Navigate to **All projects** using the menu on the left.
1. Select **+ New project**.
1. In the **Create a new project** wizard, create a project with the following settings:
    - **Current hub**: *Your AI hub*
    - **Project name**: *A unique name for your project*
1. Wait for your project to be created. When it's ready, it should look similar to the following image:

    ![Screenshot of a project details page in Azure AI Studio.](./media/azure-ai-project.png)

1. View the pages in the pane on the left side, expanding each section, and note the tasks you can perform and the resources you can manage in a project.

## Deploy and test a model

You can use a project to create complex AI solutions based on generative AI models. A full exploration of all of the development options available in Azure AI Studio is beyond the scope of this exercise, but we'll explore some basic ways in which you can work with models in a project.

1. In the pane on the left for your project, in the **Components** section, select the **Deployments** page.
1. On the **Deployments** page, in the **Model deployments** tab, select **+ Deploy model**.
1. Search for the **gpt-35-turbo** model from the list, select and confirm.
1. Deploy the model with the following settings:
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

    ![Screenshot of the playground in Azure AI Studio.](./media/playground.png)

## Clean up

If you've finished exploring Azure AI Studio, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
