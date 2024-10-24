---
lab:
    title: 'Build a custom copilots with prompt flow in the Azure AI Studio'
---

# Build a custom copilots with prompt flow in the Azure AI Studio

In this exercise, you'll use Azure AI Studio's prompt flow to create a custom copilot that uses a user prompt and chat history as inputs, and uses a GPT model from Azure OpenAI to generate an output.

This exercise will take approximately **30** minutes.

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
    - **Location**: Select **Help me choose** and then select **gpt-35-turbo** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new connection*
    - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions in the location helper include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region. Learn more about [model availability per region](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#gpt-35-turbo-model-availability)

1. Review your configuration and create your project.
1. Wait for your project to be created.

## Deploy a GPT model

To use a language model in prompt flow, you need to deploy a model first. The Azure AI Studio allows you to deploy OpenAI models that you can use in your flows.

1. In the navigation pane on the left, under **Components**, select the **Deployments** page.
1. Create a new deployment of the **gpt-35-turbo** model with the following settings:
    - **Deployment name**: *A unique name for your model deployment*
    - **Deployment type**: Standard
    - **Model version**: *Select the default version*
    - **AI resource**: *Select the resource created previously*
    - **Tokens per Minute Rate Limit (thousands)**: 5K
    - **Content filter**: DefaultV2
    - **Enable dynamic quota**: Disabled
1. Wait for the model to be deployed. When the deployment is ready, select **Open in playground**.
1. In the chat window, enter the query `What can you do?`.

    Note that the answer is generic because there are no specific instructions for the assistant. To make it focused on a task, you can change the system prompt.

1. Change the **System message** to the following:

   ```md
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

1. Select **Save**.
1. In the chat window, enter the same query as before: `What can you do?` Note the change in response.

Now that you have played around with the system message for the deployed GPT model, you can further customize the application by working with prompt flow.

## Create and run a chat flow in the Azure AI Studio

You can create a new flow from a template, or create a flow based on your configurations in the playground. Since you were already experimenting in the playground, you'll use this option to create a new flow.

<details>  
    <summary><b>Troubleshooting tip</b>: Permissions error</summary>
    <p>If you receive a permissions error when you create a new prompt flow, try the following to troubleshoot:</p>
    <ul>
        <li>In the Azure portal, select the AI Services resource.</li>
        <li>On the IAM page, in the Identity tab, confirm that it is system assigned managed identity.</li>
        <li>Navigate to the associated Storage Account. On the IAM page, add role assignment <em>Storage blob data reader</em>.</li>
        <li>Under <strong>Assign access to</strong>, choose <strong>Managed Identity</strong>, <strong>+ Select members</strong>, and select the <strong>All system-assigned managed identities</strong>.</li>
        <li>Review and assign to save the new settings and retry the previous step.</li>
    </ul>
</details>

1. In the **Chat playground**, select **Prompt flow** from the top bar.
1. Enter `Travel-Chat` as folder name.

    A simple chat flow is created for you. Note there are two inputs (chat history and the user's question), an LLM node that will connect with your deployed language model, and an output to reflect the response in the chat.

    To be able to test your flow, you need compute.

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
