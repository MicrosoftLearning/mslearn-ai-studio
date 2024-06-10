---
lab:
    title: 'Evaluate language apps in the Azure AI Studio'
---

# Evaluate language apps in the Azure AI Studio

In this exercise, you'll explore built-in and custom evaluations to assess and compare the performance of your AI applications with the Azure AI Studio.

> To complete this exercise, your Azure subscription must be approved for access to the Azure OpenAI service. Fill in the [registration form](https://learn.microsoft.com/legal/cognitive-services/openai/limited-access) to request access to Azure OpenAI models.

To build a copilot with prompt flow, you need to:

- Create an AI hub and project within the Azure AI Studio.
- Deploy a GPT model.
- Evaluate a test dataset with the built-in metrics.
- Define a custom evaluation metric and run it against the test dataset.

## Create an AI hub and project in the Azure AI Studio

You start by creating an Azure AI Studio project within an Azure AI hub:

1. In a web browser, open [https://ai.azure.com](https://ai.azure.com) and sign in using your Azure credentials.
1. Select the **Home** page, then select **+ New project**.
1. In the **Create a new project** wizard, create a project with the following settings:
    - **Project name**: *A unique name for your project*
    - **Hub**: *Create a new hub with the following settings:*
        - **Hub name**: *A unique name*
        - **Subscription**: *Your Azure subscription*
        - **Resource group**: *A new resource group*
        - **Location**: *Make a **random** choice from any of the following regions*\*
        - Australia East
        - Canada East
        - East US
        - East US 2
        - France Central
        - Japan East
        - North Central US
        - Sweden Central
        - Switzerland North
        - UK South
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new connection*
    - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region. Learn more about [model availability per region](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#gpt-35-turbo-model-availability)

1. Review your configuration and create your project.
1. Wait 5-10 minutes for your project to be created.

## Deploy a GPT model

To use a language model in prompt flow, you need to deploy a model first. The Azure AI Studio allows you to deploy OpenAI models that you can use in your flows.

1. In the navigation pane on the left, under **Components**, select the **Deployments** page.
1. Create a new deployment of the **gpt-35-turbo** model with the following settings:
    - **Deployment name**: *A unique name for your model deployment*
    - **Model version**: *Select the default version*
    - **Deployment type**: Standard
    - **Connected Azure OpenAI resource**: *Select the default connection*
    - **Tokens per Minute Rate Limit (thousands)**: 5K
    - **Content filter**: Default
1. Wait for the model to be deployed. When the deployment is ready, select **Open in playground**.
1. Change the **System message** to the following:

   ```
   **Objective**: Assist users with travel-related inquiries, offering tips, advice, and recommendations as a knowledgeable travel agent.

   **Capabilities**:
   - Provide up-to-date travel information, including destinations, accommodations, transportation, and local attractions.
   - Offer personalized travel suggestions based on user preferences, budget, and travel dates.
   - Share tips on packing, safety, and navigating travel disruptions.
   - Help with itinerary planning, including optimal routes and must-see landmarks.
   - Answer common travel questions and provide solutions to potential travel issues.
    
   **Instructions**:
   1. Engage with the user in a friendly and professional manner, as a travel agent would.
   2. Use available resources to provide accurate and relevant travel information.
   3. Tailor responses to the user's specific travel needs and interests.
   4. Ensure recommendations are practical and consider the user's safety and comfort.
   5. Encourage the user to ask follow-up questions for further assistance.
   ```

1. Select **Apply changes**.
1. In the chat window, enter the query: `What can you do?` to verify that the language model is behaving as expected.

Now that you have a deployed model with an updated system message, you can evaluate the model.

## Evaluate a language model in the Azure AI Studio

You can manually review model responses based on test data. Manually reviewing allows you to test different inputs one at a time to evaluate whether the model performs as expected.

1. In the **Chat playground**, select **Evaluate** from the top bar.
1. A new window opens with your previous system message already populated and your deployed model selected.
1. Select **Import test data**. Select **Import without saving** if prompted.
1. Select **Upload file** and 
1. Select **Start compute session** from the top bar.
1. The compute session will take 1-3 minutes to start.
1. Find the LLM node named **chat**. Note that the prompt already includes the system prompt you specified in the chat playground.

    You still need to connect the LLM node to your deployed model.

1. In the LLM node section, for **Connection**, select the connection that was created for you when you created the AI hub.
1. For **Api**, select **chat**.
1. For **deployment_name**, select the **gpt-35-turbo** model you deployed.
1. For **response_format**, select **{"type":"text"}**.
1. Review the prompt field and ensure it looks like the following:

   ```yml
   {% raw %}
   system:
   **Objective**: Assist users with travel-related inquiries, offering tips, advice, and recommendations as a knowledgeable travel agent.

   **Capabilities**:
   - Provide up-to-date travel information, including destinations, accommodations, transportation, and local attractions.
   - Offer personalized travel suggestions based on user preferences, budget, and travel dates.
   - Share tips on packing, safety, and navigating travel disruptions.
   - Help with itinerary planning, including optimal routes and must-see landmarks.
   - Answer common travel questions and provide solutions to potential travel issues.

   **Instructions**:
   1. Engage with the user in a friendly and professional manner, as a travel agent would.
   2. Use available resources to provide accurate and relevant travel information.
   3. Tailor responses to the user's specific travel needs and interests.
   4. Ensure recommendations are practical and consider the user's safety and comfort.
   5. Encourage the user to ask follow-up questions for further assistance.

   {% for item in chat_history %}
   user:
   {{item.inputs.question}}
   assistant:
   {{item.outputs.answer}}
   {% endfor %}

   user:
   {{question}}
   {% endraw %}
   ```

### Test and deploy the flow

Now that you've developed the flow, you can use the chat window to test the flow.

1. Ensure the compute session is running.
1. Select **Save**.
1. Select **Chat** to test the flow.
1. Enter the query: `I have one day in London, what should I do?` and review the output.

    When you're satisfied with the behavior of the flow you created, you can deploy the flow.

1. Select **Deploy** to deploy the flow with the following settings:
    - **Basic settings**:
        - **Endpoint**: New
        - **Endpoint name**: *Enter a unique name*
        - **Deployment name**: *Enter a unique name*
        - **Virtual machine**: Standard_DS3_v2
        - **Instance count**: 3
        - **Inferencing data collection**: Enabled
    - **Advanced settings**:
        - *Use the default settings*
1. In Azure AI Studio, in your project, in the navigation pane on the left, under **Components**, select the **Deployments** page.
1. Note that by default the **Model deployments** are listed, including your deployed language model.
1. Select the **App deployments** tab to find your deployed flow. It may take some time before the deployment is listed and successfully created.
1. When the deployment has succeeded, select it. Then, on its **Test** page, enter the prompt `What is there to do in San Francisco?` and review the response.
1. Enter the prompt `Where else could I go?` and review the response.
1. View the **Consume** page for the endpoint, and note that it contains connection information and sample code that you can use to build a client application for your endpoint - enabling you to integrate the prompt flow solution into an application as a custom copilot.

## Delete Azure resources

When you finish exploring the Azure AI Studio, you should delete the resources you’ve created to avoid unnecessary Azure costs.

- Navigate to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`.
- In the Azure portal, on the **Home** page, select **Resource groups**.
- Select the resource group that you created for this exercise.
- At the top of the **Overview** page for your resource group, select **Delete resource group**.
- Enter the resource group name to confirm you want to delete it, and select **Delete**.
