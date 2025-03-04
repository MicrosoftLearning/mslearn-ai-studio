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

## Create an Azure AI hub and project

You can create an Azure AI hub and project manually through the Azure AI Foundry portal, as well as deploy the models used in the exercise. However, you can also automate this process through the use of a template application with [Azure Developer CLI (azd)](https://aka.ms/azd).

1. In a web browser, open [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and sign in using your Azure credentials.

1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal. For more information about using the Azure Cloud Shell, see the [Azure Cloud Shell documentation](https://docs.microsoft.com/azure/cloud-shell/overview).

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the PowerShell pane, enter the following commands to clone this exercise's repo:

     ```powershell
    rm -r mslearn-ai-studio -f
    git clone https://github.com/MicrosoftLearning/mslearn-ai-studio
     ```

1. After the repo has been cloned, enter the following commands to initialize the Starter template.

     ```powershell
    cd ./mslearn-ai-studio/Starter
    azd init
     ```

1. Once prompted, give the new environment a name as it will be used as basis for giving unique names to all the provisioned resources.

1. Next, enter the following command to run the Starter template. It will provision an AI Hub with dependent resources, AI project, AI Services and an online endpoint. It will also deploy the models GPT-4 Turbo, GPT-4o, and GPT-4o mini.

     ```powershell
    azd up  
     ```

1. When prompted, choose which subscription you want to use and then choose one of the following locations for resource provision:
   - North Central US
   - Sweden Central

1. Wait for the script to complete - this typically takes around 10 minutes, but in some cases may take longer.

     > **Note**: Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions in the location helper include default quota for the model type(s) used in this exercise. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region. Learn more about [Fine-tuning model regions](https://learn.microsoft.com/azure/ai-services/openai/concepts/models?tabs=python-secure%2Cglobal-standard%2Cstandard-chat-completions#fine-tuning-models)

    <details>
      <summary><b>Troubleshooting tip</b>: No quota available in a given region</summary>
        <p>If you receive a deployment error for any of the models due to no quota available in the region you chose, try running the following commands:</p>
        <ul>
          <pre><code>azd env set AZURE_ENV_NAME new_env_name
   azd env set AZURE_RESOURCE_GROUP new_rg_name
   azd env set AZURE_LOCATION new_location
   azd up</code></pre>
        Replacing <code>new_env_name</code>, <code>new_rg_name</code>, and <code>new_location</code> with new values. The new location must be one of the regions listed at the beginning of the exercise, e.g <code>eastus2</code>, <code>northcentralus</code>, etc.
        </ul>
    </details>

1. Once all resources have been provisioned, use the following commands to fetch the endpoint and access key to your AI Services resource. Note that you must replace `<rg-env_name>` and `<aoai-xxxxxxxxxx>` with the names of your resource group and AI Services resource. Both are printed in the deployment's output.

     ```powershell
    Get-AzCognitiveServicesAccount -ResourceGroupName <rg-env_name> -Name <aoai-xxxxxxxxxx> | Select-Object -Property endpoint
    Get-AzCognitiveServicesAccountKey -ResourceGroupName <rg-env_name> -Name <aoai-xxxxxxxxxx> | Select-Object -Property Key1
     ```

1. Copy these values as they will be used later on.

## Set up your local development environment

To quickly experiment and iterate, you'll use a notebook with Python code in Visual Studio (VS) Code. Let's get VS Code ready to use for local ideation.

1. Open VS Code and **Clone** the following Git repo: `https://github.com/MicrosoftLearning/mslearn-ai-studio`
1. Store the clone on a local drive, and open the folder after cloning.
   
## Fine-tune a GPT-4 model

Because fine-tuning a model takes some time to complete, you'll start the fine-tuning job now and come back to it after exploring a base model that has not been fine-tuned for comparison purposes.

1. In the VS Code Explorer (left pane), open the script **fine-tune-app.py** in the **labfiles/fine-tune-app/Python** folder.
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
