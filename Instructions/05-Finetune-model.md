---
lab:
    title: 'Fine-tune a language model for chat completion in the Azure AI Foundry'
---

# Fine-tune a language model for chat completion in the Azure AI Foundry

When you want a language model to behave a certain way, you can use prompt engineering to define the desired behavior. When you want to improve the consistency of the desired behavior, you can opt to fine-tune a model, comparing it to your prompt engineering approach to evaluate which method best fits your needs.

In this exercise, you'll fine-tune a language model with the Azure AI Foundry that you want to use for a custom chat application scenario. You'll compare the fine-tuned model with a base model to assess whether the fine-tuned model fits your needs better.

Imagine you work for a travel agency and you're developing a chat application to help people plan their vacations. The goal is to create a simple and inspiring chat that suggests destinations and activities. Since the chat isn't connected to any data sources, it should **not** provide specific recommendations for hotels, flights, or restaurants to ensure trust with your customers.

This exercise will take approximately **60** minutes.

## Create an AI hub and project in the Azure AI Foundry portal

You start by creating an Azure AI Foundry portal project within an Azure AI hub:

1. In a web browser, open [https://ai.azure.com](https://ai.azure.com) and sign in using your Azure credentials.
1. From the home page, select **+ Create project**.
1. In the **Create a new project** wizard, create a project with the following settings:
    - **Project name**: *A unique name for your project*
    - Select **Customize**
        - **Hub**: *Autofills with default name*
        - **Subscription**: *Autofills with your signed in account*
        - **Resource group**: (New) *Autofills with your project name*
        - **Location**: Choose one of the following regions **East US2**, **North Central US**, **Sweden Central**, **Switzerland West**\*
        - **Connect Azure AI Services or Azure OpenAI**: (New) *Autofills with your selected hub name*
        - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions in the location helper include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region. Learn more about [Fine-tuning model regions](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=python-secure%2Cglobal-standard%2Cstandard-chat-completions#fine-tuning-models)

1. Review your configuration and create your project.
1. Wait for your project to be created.

## Fine-tune a GPT-3.5 model

As fine-tuning a model takes some time to complete, you'll start the fine-tuning job first. Before you can fine-tune a model, you need a dataset.

1. Download the [training dataset](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/refs/heads/main/data/travel-finetune-hotel.jsonl) at `https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/refs/heads/main/data/travel-finetune-hotel.jsonl`and save it as a JSONL file locally.

    > **Note**: Your device might default to saving the file as a .txt file. Select all files and remove the .txt suffix to ensure you're saving the file as JSONL.

1. Navigate to the **Fine-tuning** page under the **Build and customize** section, using the menu on the left.
1. Select the button to add a new fine-tune model, select the `gpt-35-turbo` model, select **Next** and then **Confirm**.
1. **Fine-tune** the model using the following configuration:
    - **Model version**: *Select the default version*
    - **Model suffix**: `ft-travel`
    - **Connected AI resource**: *Select the connection that was created when you created your hub. Should be selected by default.*
    - **Training data**: Upload files

    <details>  
    <summary><b>Troubleshooting tip</b>: Permissions error</summary>
    <p>If you receive a permissions error, try the following to troubleshoot:</p>
    <ul>
        <li>In the Azure portal, select the AI Services resource.</li>
        <li>Under Resource Management, in the Identity tab, confirm that it is system assigned managed identity.</li>
        <li>Navigate to the associated Storage Account. On the IAM page, add role assignment <em>Storage Blob Data Owner</em>.</li>
        <li>Under <strong>Assign access to</strong>, choose <strong>Managed Identity</strong>, <strong>+ Select members</strong>, select the <strong>All system-assigned managed identities</strong>, and select your Azure AI services resource.</li>
        <li>Review and assign to save the new settings and retry the previous step.</li>
    </ul>
    </details>

    - **Upload file**: Select the JSONL file you downloaded in a previous step.
    - **Validation data**: None
    - **Task parameters**: *Keep the default settings*
1. Fine-tuning will start and may take some time to complete.

> **Note**: Fine-tuning and deployment can take some time, so you may need to check back periodically. You can already continue with the next step while you wait.

## Chat with a base model

While you wait for the fine-tuning job to complete, let's chat with a base GPT 3.5 model to assess how it performs.

1. Navigate to the **Models + endpoints** page under the **My assets** section, using the menu on the left.
1. Select the **+ Deploy model** button, and select the **Deploy base model** option.
1. Deploy a `gpt-35-turbo` model, which is the same type of model you used when fine-tuning.

> **Note**: If your current AI resource location doesn't have quota available for the model you want to deploy, you will be asked to choose a different location where a new AI resource will be created and connected to your project.

1. When deployment is completed, select the **Open in playground** button.
1. Verify your deployed `gpt-35-model` base model is selected in setup pane.
1. In the chat window, enter the query `What can you do?` and view the response.
    The answers are very generic. Remember we want to create a chat application that inspires people to travel.
1. Update the system message in the setup pane with the following prompt:

    ```md
    You are an AI assistant that helps people plan their holidays.
    ```

1. Select **Apply changes**, then select **Clear chat**, and ask again `What can you do?`
    As a response, the assistant may tell you that it can help you book flights, hotels and rental cars for your trip. You want to avoid this behavior.
1. Update the system message again with a new prompt:

    ```md
    You are an AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms.
    You should not provide any hotel, flight, rental car or restaurant recommendations.
    Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday.
    ```

1. Select **Apply changes**, and **Clear chat**.
1. Continue testing your chat application to verify it doesn't provide any information that isn't grounded in retrieved data. For example, ask the following questions and explore the model's answers:
   
    `Where in Rome should I stay?`
    
    `I'm mostly there for the food. Where should I stay to be within walking distance of affordable restaurants?`

    `Give me a list of five bed and breakfasts in Trastevere.`

    The model may provide you with a list of hotels, even when you instructed it not to give hotel recommendations. This is an example of inconsistent behavior. Let's explore whether the fine-tuned model performs better in these cases.

1. Navigate to the **Fine-tuning** page under **Build and customize** to find your fine-tuning job and its status. If it's still running, you can opt to continue manually evaluating your deployed base model. If it's completed, you can continue with the next section.

## Deploy the fine-tuned model

When fine-tuning has successfully completed, you can deploy the fine-tuned model.

1. Select the fine-tuned model. Select the **Metrics** tab and explore the fine-tune metrics.
1. Deploy the fine-tuned model with the following configurations:
    - **Deployment name**: *A unique name for your model, you can use the default*
    - **Deployment type**: Standard
    - **Tokens per Minute Rate Limit (thousands)**: 5K
    - **Content filter**: Default
1. Wait for the deployment to be complete before you can test it, this may take a while.

## Test the fine-tuned model

Now that you deployed your fine-tuned model, you can test it like you tested your deployed base model.

1. When the deployment is ready, navigate to the fine-tuned model and select **Open in playground**.
1. Update the system message with the following instructions:

    ```md
    You are an AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms.
    You should not provide any hotel, flight, rental car or restaurant recommendations.
    Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday.
    ```

1. Test your fine-tuned model to assess whether its behavior is more consistent now. For example, ask the following questions again and explore the model's answers:
   
    `Where in Rome should I stay?`
    
    `I'm mostly there for the food. Where should I stay to be within walking distance of affordable restaurants?`

    `Give me a list of five bed and breakfasts in Trastevere.`

## Clean up

If you've finished exploring Azure AI Foundry, you should delete the resources you've created to avoid unnecessary Azure costs.

- Navigate to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`.
- In the Azure portal, on the **Home** page, select **Resource groups**.
- Select the resource group that you created for this exercise.
- At the top of the **Overview** page for your resource group, select **Delete resource group**.
- Enter the resource group name to confirm you want to delete it, and select **Delete**.
