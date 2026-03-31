---
lab:
  title: Fine-tune a language model
  description: Learn how to use your own training data to fine-tune a model and customize its behavior.
  level: 300
  duration: 90
  islab: true
---

# Fine-tune a language model

When you want a language model to behave a certain way, you can use prompt engineering to define the desired behavior. When you want to improve the consistency of the desired behavior, you can opt to fine-tune a model, comparing it to your prompt engineering approach to evaluate which method best fits your needs.

In this exercise, you'll fine-tune a language model with Microsoft Foundry that you want to use for a custom chat application scenario. You'll compare the fine-tuned model with a base model to assess whether the fine-tuned model fits your needs better.

Imagine you work for a travel agency and you're developing a chat application to help people plan their vacations. The goal is to create a simple and inspiring chat that suggests destinations and activities with a consistent, friendly conversational tone.

This exercise will take approximately **90** minutes\*.

> \* **Note**: This timing is an estimate based on the average experience. Fine-tuning is dependent on cloud infrastructure resources, which can take a variable amount of time to provision depending on data center capacity and concurrent demand. Some activities in this exercise may take a <u>long</u> time to complete, and require patience. If things are taking a while, consider reviewing the [Microsoft Foundry fine-tuning documentation](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry) or taking a break. It is possible some processes may time-out or appear to run indefinitely. Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Prerequisites

To complete this exercise, you need:

- An [Azure subscription](https://azure.microsoft.com/free/) with permissions to create AI resources.

## Create a Microsoft Foundry project

Microsoft Foundry uses projects to organize models, resources, data, and other assets used to develop an AI solution.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the Foundry logo at the top left to navigate to the home page.

1. If it is not already enabled, in the tool bar the top of the page, enable the **New Foundry** option. Then, if prompted, create a new project with a unique name; expanding the **Advanced options** area to specify the following settings for your project:
    - **Foundry resource**: *Use the default name for your resource (usually {project_name}-resource)*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Region**: *Select one of the following regions*:\*
        - North Central US
        - Sweden Central

    > \* At the time of writing, these regions support fine-tuning for gpt-4.1 models. Check the [models page](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure?&pivots=azure-openai#fine-tuning-models) for the latest region availability.

1. Wait for your project to be created. Then view its home page.

## Deploy a model

Now deploy a model that you'll use to get a performance baseline.

1. Now you're ready to **Start building**. Select **Find models** (or on the **Discover** page, select the **Models** tab) to view the Microsoft Foundry model catalog.
1. In the model catalog, search for `gpt-4.1`.
1. Review the model card, and then deploy it using the default settings.
1. When the model has been deployed, it will open in the model playground.

## Fine-tune a model

Because fine-tuning a model takes some time to complete, you'll start the fine-tuning job now and come back to it after exploring the base gpt-4.1 model you already deployed.

1. Download the [training dataset](https://microsoftlearning.github.io/mslearn-ai-studio/data/travel-finetune-hotel.jsonl) at `https://microsoftlearning.github.io/mslearn-ai-studio/data/travel-finetune-hotel.jsonl` and save it as a JSONL file locally.

    > **Note**: Your device might default to saving the file as a .txt file. Select all files and remove the .txt suffix to ensure you're saving the file as JSONL.

1. In the Foundry portal, while viewing the model playground, left navigation pane, select **Fine-tune**.
1. Select the **Fine-tune** button at the upper right, and then configure the fine-tuning job with the following settings:
    - **Base model**: Select **gpt-4.1**
    - **Customization method**: Supervised
    - **Training type**: Standard
    - **Training data**: Select **Upload new dataset** and upload the .jsonl file you downloaded previously.
    - **Suffix**: `ft-travel`
    - **Automatically deploy model after job completion**: Selected
    - **Deployment type**: Developer
    - *Leave the remaining hyperparameters at their defaults*
1. Select **Submit** to start the fine-tuning job. It may take some time to complete. You can continue with the next section of the exercise while you wait.

> **Note**: Fine-tuning and deployment can take a significant amount of time (60 minutes or longer), so you may need to check back periodically. You can see more details of the progress so far by selecting the fine-tuning job and viewing its **Monitor** tab.

## Chat with a base model

While you wait for the fine-tuning job to complete, let's chat with a *gpt-4.1* foundation model to assess how it performs.

1. In the left pane, select **Models** and then select the **gpt-4.1** base model you deployed previously.
1. In the chat pane, enter the prompt `What can you do?` and view the response.

    The answers may be fairly generic. Remember we want to create a chat application that inspires people to travel.

1. Change the model **Instructions** to the following prompt:

    ```
   You are an AI assistant that helps people plan their travel.
    ```

1. In the chat window, enter the query `What can you do?` again, and view the response.

    As a response, the assistant may tell you that it can help you book flights, hotels and rental cars for your trip. You want to avoid this behavior.

1. In the **Instructions** field, enter a new prompt:

    ```
   You are an AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms.
   You should not provide any hotel, flight, rental car or restaurant recommendations.
   Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday.
    ```

1. Continue testing the model to review its behavior. For example, ask the following questions and note the model's answers, paying particular attention to the tone and writing style that the model uses to respond:

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

## Test the fine-tuned model

When your fine-tuned model is ready, you can test it like you tested your deployed base model.

1. In the pane on the left, select **Fine-tune** and review the status of the fine-tuning job you started earlier.
1. Select the job to view its details. You can use the **Logs** tab to review the fine-tuning tasks that have been performed so far.
1. When fine-tuning is complete, and the model has been automatically deployed, view the **Models** page to verify that it is listed.

    > **Tip**: If automatic deployment fails, select the completed fine-tuning job and deploy the model from there.
1. Select the fine-tuned model to open it in the model playground.
1. Update the **Instructions** to be the same as you tested with the base model:

    ```
   You are an AI travel assistant that helps people plan their trips. Your objective is to offer support for travel-related inquiries, such as visa requirements, weather forecasts, local attractions, and cultural norms.
   You should not provide any hotel, flight, rental car or restaurant recommendations.
   Ask engaging questions to help someone plan their trip and think about what they want to do on their holiday.
    ```

1. Test your fine-tuned model to assess whether its behavior is more consistent than the base model. For example, ask the following questions again and explore the model's answers:

    `Where in Rome should I stay?`

    `I'm mostly there for the food. Where should I stay to be within walking distance of affordable restaurants?`

    `What are some local delicacies I should try?`

    `When is the best time of year to visit in terms of the weather?`

    `What's the best way to get around the city?`

## Clean up

If you've finished exploring Microsoft Foundry, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
