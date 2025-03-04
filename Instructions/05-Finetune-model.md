---
lab:
    title: 'Fine-tune a language model'
    description: 'Learn how to use your own additional training data to fine-tune a model and customize its behavior.'
---

# Fine-tune a language model

When you want a language model to behave a certain way, you can use prompt engineering to define the desired behavior. When you want to improve the consistency of the desired behavior, you can opt to fine-tune a model, comparing it to your prompt engineering approach to evaluate which method best fits your needs.

In this exercise, you'll fine-tune a language model with the Azure AI Foundry that you want to use for a custom chat application scenario. You'll compare the fine-tuned model with a base model to assess whether the fine-tuned model fits your needs better.

Imagine you work for a travel agency and you're developing a chat application to help people plan their vacations. The goal is to create a simple and inspiring chat that suggests destinations and activities. Since the chat isn't connected to any data sources, it should **not** provide specific recommendations for hotels, flights, or restaurants to ensure trust with your customers.

This exercise will take approximately **60** minutes\*.

> \* **Note**: This timing is an estimate based on the average experience. Fine-tuning is dependent on cloud infrastructure resources, which can take a variable amount of time to provision depending on data center capacity and concurrent demand. Some activities in this exercise may take a <u>long</u> time to complete, and require patience. If things are taking a while, consider reviewing the [Azure AI Foundry fine-tuning documentation](https://learn.microsoft.com/azure/ai-studio/concepts/fine-tuning-overview) or taking a break.

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
        -  **Location**: Select **Help me choose** and then select **gpt-4-finetune** in the Location helper window and use the recommended region\*
        - **Connect Azure AI Services or Azure OpenAI**: (New) *Autofills with your selected hub name*
        - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions in the location helper include default quota for the model type(s) used in this exercise. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region. Learn more about [Fine-tuning model regions](https://learn.microsoft.com/azure/ai-services/openai/concepts/models?tabs=python-secure%2Cglobal-standard%2Cstandard-chat-completions#fine-tuning-models)

1. Review your configuration and create your project.
1. Wait for your project to be created.

## Fine-tune a GPT-4 model

Because fine-tuning a model takes some time to complete, you'll start the fine-tuning job now and come back to it after exploring a base model that has not been fine-tuned for comparison purposes.

1. Download the [training dataset](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/refs/heads/main/data/travel-finetune-hotel.jsonl) at `https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/refs/heads/main/data/travel-finetune-hotel.jsonl`and save it as a JSONL file locally.

    > **Note**: Your device might default to saving the file as a .txt file. Select all files and remove the .txt suffix to ensure you're saving the file as JSONL.

1. Navigate to the **Fine-tuning** page under the **Build and customize** section, using the menu on the left.
1. Select the button to add a new fine-tune model, select the `gpt-4` model, select **Next** and then **Confirm**.
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

> **Note**: Fine-tuning and deployment can take a significant amount of time (30 minutes or longer), so you may need to check back periodically. You can already continue with the next step while you wait.

## Chat with a base model

While you wait for the fine-tuning job to complete, let's chat with a base GPT 4 model to assess how it performs.

1. Navigate to the **Models + endpoints** page under the **My assets** section, using the menu on the left.
1. Select the **+ Deploy model** button, and select the **Deploy base model** option.
1. Deploy a `gpt-4` model with the following settings:
    - **Deployment name**: *A unique name for your model, you can use the default*
    - **Deployment type**: Standard
    - **Tokens per Minute Rate Limit (thousands)**: 5K
    - **Content filter**: Default

> **Note**: If your current AI resource location doesn't have quota available for the model you want to deploy, you will be asked to choose a different location where a new AI resource will be created and connected to your project.

1. When deployment is completed, select the **Open in playground** button.
1. Verify your deployed `gpt-4` base model is selected in setup pane.
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
1. Continue testing your chat application to verify it doesn't provide any information that isn't grounded in retrieved data. For example, ask the following questions and review the model's answers, paying particular attention to the tone and writing style that the model uses to respond:
   
    `Where in Rome should I stay?`
    
    `I'm mostly there for the food. Where should I stay to be within walking distance of affordable restaurants?`

    `What are some local delicacies I should try?`

    `When is the best time of year to visit in terms of the weather?`

    `What's the best way to get around the city?`

## Review the training file

The base model seems to work well enough, but you may be looking for a particular conversational style from your generative AI app. The training data used for fine-tuning offers you the chance to create explicit examples of the kinds of response you want.

1. Open the JSONL file you downloaded previously (you can open it in any text editor)
1. Examine the list of the JSON documents in the training data file. The first one should be similar to this (formatted for readability):

    ```json
    {"messages": [
        {"role": "system", "content": "You are an AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms. You should not provide any hotel, flight, rental car or restaurant recommendations. Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday."},
        {"role": "user", "content": "What's a must-see in Paris?"},
        {"role": "assistant", "content": "Oh la la! You simply must twirl around the Eiffel Tower and snap a chic selfie! After that, consider visiting the Louvre Museum to see the Mona Lisa and other masterpieces. What type of attractions are you most interested in?"}
        ]}
    ```

    Each example interaction in the list includes the same system message you tested with the base model, a user prompt related to a travel query, and a response. The style of the responses in the training data will help the fine-tuned model learn how it should respond.

## Deploy the fine-tuned model

When fine-tuning has successfully completed, you can deploy the fine-tuned model.

1. Navigate to the **Fine-tuning** page under **Build and customize** to find your fine-tuning job and its status. If it's still running, you can opt to continue chatting with your deployed base model or take a break. If it's completed, you can continue.
1. Select the fine-tuned model. Select the **Metrics** tab and explore the fine-tune metrics.
1. Deploy the fine-tuned model with the following configurations:
    - **Deployment name**: *A unique name for your model, you can use the default*
    - **Deployment type**: Standard
    - **Tokens per Minute Rate Limit (thousands)**: 5K
    - **Content filter**: Default
1. Wait for the deployment to be complete before you can test it, this might take a while. Check the **Provisioning state** until it has succeeded (you may need to refresh the browser to see the updated status).

## Test the fine-tuned model

Now that you deployed your fine-tuned model, you can test it like you tested your deployed base model.

1. When the deployment is ready, navigate to the fine-tuned model and select **Open in playground**.
1. Ensure the system message includes these instructions:

    ```md
    You are an AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms.
    You should not provide any hotel, flight, rental car or restaurant recommendations.
    Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday.
    ```

1. Test your fine-tuned model to assess whether its behavior is more consistent now. For example, ask the following questions again and explore the model's answers:
   
    `Where in Rome should I stay?`
    
    `I'm mostly there for the food. Where should I stay to be within walking distance of affordable restaurants?`

    `What are some local delicacies I should try?`

    `When is the best time of year to visit in terms of the weather?`

    `What's the best way to get around the city?`

1. After reviewing the responses, how do they compare to those of the base model?

## Clean up

If you've finished exploring Azure AI Foundry, you should delete the resources you've created to avoid unnecessary Azure costs.

- Navigate to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`.
- In the Azure portal, on the **Home** page, select **Resource groups**.
- Select the resource group that you created for this exercise.
- At the top of the **Overview** page for your resource group, select **Delete resource group**.
- Enter the resource group name to confirm you want to delete it, and select **Delete**.
