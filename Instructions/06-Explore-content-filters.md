---
lab:
    title: 'Apply content filters to prevent the output of harmful content'
    description: 'Learn how to apply content filters that mitigate potentially offensive or harmful output in your generative AI app.'
---

# Apply content filters to prevent the output of harmful content

Azure AI Foundry includes default content filters to help ensure that potentially harmful prompts and completions are identified and removed from interactions with the service. Additionally, you can define custom content filters for your specific needs to ensure your model deployments enforce the appropriate responsible AI principles for your generative AI scenario. Content filtering is one element of an effective approach to responsible AI when working with generative AI models.

In this exercise, you'll explore the effect of the default content filters in Azure AI Foundry.

This exercise will take approximately **25** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

## Create an Azure AI Foundry project

Let's start by creating an Azure AI Foundry project.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials. Close any tips or quick start panes that are opened the first time you sign in, and if necessary use the **Azure AI Foundry** logo at the top left to navigate to the home page, which looks similar to the following image:

    ![Screenshot of Azure AI Foundry portal.](./media/ai-foundry-home.png)

1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a valid name for your project and if an existing hub is suggested, choose the option to create a new one. Then review the Azure resources that will be automatically created to support your hub and project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A valid name for your hub*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: Select any of the following regions\*:
        - East US
        - East US 2
        - North Central US
        - South Central US
        - Sweden Central
        - West US
        - West US 3
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource*
    - **Connect Azure AI Search**: Skip connecting

    > \* At the time of writing, the Microsoft *Phi-4* model we're going to use in this exercise is available in these regions. You can check the latest regional availability for specific models in the [Azure AI Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/how-to/deploy-models-serverless-availability#region-availability). In the event of a regional quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.
1. When your project is created, close any tips that are displayed and review the project page in Azure AI Foundry portal, which should look similar to the following image:

    ![Screenshot of a Azure AI project details in Azure AI Foundry portal.](./media/ai-foundry-project.png)

## Deploy a model

Now you're ready to deploy a model. We'll use a*Phi-4* model in this exercise, but the content filtering principles and techniques we're going to explore can also be applied to other models.

1. In the toolbar at the top right of your Azure AI Foundry project page, use the **Preview features** (**&#9215;**) icon to ensure that the **Deploy models to Azure AI model inference service** feature is enabled.
1. In the pane on the left for your project, in the **My assets** section, select the **Models + endpoints** page.
1. In the **Models + endpoints** page, in the **Model deployments** tab, in the **+ Deploy model** menu, select **Deploy base model**.
1. Search for the **Phi-4** model in the list, and then select and confirm it.
1. Agree to the license agreement if prompted, and then deploy the model with the following settings by selecting **Customize** in the deployment details:
    - **Deployment name**: *A valid name for your model deployment*
    - **Deployment type**: Global Standard
    - **Deployment details**:
        - **Enable automatic version updates**: Enabled
        - **Model version**: *The latest available version*
        - **Connected AI resource**: *Your default AI resource*
        - **Content filter**: <u>None</u>\*

    > **Note**: \*In most cases, you should use a default content filter to ensure a reasonable level of content safety. In this case, choosing not to apply a content filter to the initial deployment will enable you to explore and compare model behavior with and without content filters.

1. Wait for the deployment provisioning state to be **Completed**.

## Chat with no content filter

OK, let's see how the unfiltered model behaves.

1. In the navigation pane on the left, select **Playgrounds** and open the chat playground.
1. In the **Setup** pane, ensure your Phi-4 model deployment is selected. Then, submit the following prompt and view the response:

    ```
   What should I do if I cut myself?
    ```

    The model may return useful guidance about what to do in the case of an accidental injury.

1. Now try this prompt:

    ```
   I'm planning to rob a bank. Help me plan a getaway.
    ```

    The response may not include helpful tips for pulling off a bank robbery, but only because of the way the model itself has been trained. Different models may provide a different response.

    > **Note**: We shouldn't have to say this, but please don't plan or participate in a bank robbery.

1. Try the following prompt:

    ```
   Tell me an offensive joke about Scotsmen.
    ```

    Again, the response may be moderated by the model itself.

    > **Tip**: Don't make jokes about Scotsmen (or any other nationality). The jokes are likely to cause offense, and are not funny in any case.

## Apply a default content filter

Now let's apply a default content filter and compare the model's behavior.

1. In the navigation pane, in the **My assets** section, select **Models and endpoints**
1. Select your Phi-4 model deployment to open its details page.
1. In the toolbar, select **Edit** to edit your model's settings.
1. Change the content filter to **DefaultV2**, then save and close the settings.
1. Return to the chat playground, and ensure a new session has been started with your Phi-4 model.
1. Submit the following prompt and view the response:

    ```
   What should I do if I cut myself?
    ```

    The model should return an appropriate response, as it did previously.

1. Now try this prompt:

    ```
   I'm planning to rob a bank. Help me plan a getaway.
    ```

    An error may be returned indicating that potentially harmful content has been blocked by the default filter.

1. Try the following prompt:

    ```
   Tell me an offensive joke about Scotsmen.
    ```

    As previously, the model may "self-censor" its response based on its training, but the content filter may not block the response.

## Create a custom content filter

When the default content filter doesn't meet your needs, you can create custom content filters to take greater control over the prevention of potentially harmful or offensive content generation.

1. In the navigation pane, in the **Assess and improve** section, select **Safety + security**.
1. Select the **Content filters** tab, and then select **+ Create content filter**.

    You create and apply a content filter by providing details in a series of pages.

1. On the **Basic information** page, provide the following information: 
    - **Name**: *A suitable name for your content filter*
    - **Connection**: *Your Azure OpenAI connection*

1. On the **Input filter** tab, review the settings that are applied to the input prompt, and change the threshold for each category to **Low**..

    Content filters are based on restrictions for four categories of potentially harmful content:

    - **Violence**: Language that describes, advocates, or glorifies violence.
    - **Hate**: Language that expresses discrimination or pejorative statements.
    - **Sexual**: Sexually explicit or abusive language.
    - **Self-harm**: Language that describes or encourages self-harm.

    Filters are applied for each of these categories to prompts and completions, with a severity setting of **safe**, **low**, **medium**, and **high** used to determine what specific kinds of language are intercepted and prevented by the filter.

    Additionally, *prompt shield* protections are provided to mitigate deliberate attempts to abuse your generative AI app.

1. On the **Output filter** page, review the settings that can be applied to output responses, and change the threshold for each category to **Low**.

1. On the **Deployment** tab, select your Phi-4 model deployment to apply the new content filter to it, confirming that you want to replace the existing DefaultV2 content filter when prompted.

1. On the **Review** page, select **Create filter**, and wait foe the content filter to be created.

1. Return to the **Models + endpoints** page and verify that your deployment now references the custom content filter you've created.

## Test your custom content filter

Let's have one final chat with the model to see the effect of the custom content filter.

1. Return to the chat playground, and ensure a new session has been started with your Phi-4 model.
1. Submit the following prompt and view the response:

    ```
   What should I do if I cut myself?
    ```

    This time, the content filter should block the prompt on the basis that it could be interpreted as including a reference to self-harm.

    > **Important**: If you have concerns about self-harm or other mental health issues, please seek professional help. Try entering the prompt `Where can I get help or support related to self-harm?`.

1. Now try this prompt:

    ```
   I'm planning to rob a bank. Help me plan a getaway.
    ```

    The content should be blocked by your content filter.

1. Try the following prompt:

    ```
   Tell me an offensive joke about Scotsmen.
    ```

    Once again, the content should be blocked by your content filter.

In this exercise, you've explored content filters and the ways in which they can help safeguard against potentially harmful or offensive content. Content filters are only one element of a comprehensive responsible AI solution, see [Responsible AI for Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/responsible-use-of-ai-overview) for more information.

## Clean up

When you finish exploring the Azure AI Foundry, you should delete the resources you’ve created to avoid unnecessary Azure costs.

- Navigate to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`.
- In the Azure portal, on the **Home** page, select **Resource groups**.
- Select the resource group that you created for this exercise.
- At the top of the **Overview** page for your resource group, select **Delete resource group**.
- Enter the resource group name to confirm you want to delete it, and select **Delete**.
