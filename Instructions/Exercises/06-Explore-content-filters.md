---
lab:
  title: Apply guardrails to prevent the output of harmful content
  description: Learn how to apply content filters that mitigate potentially offensive or harmful output in your generative AI app.
  level: 300
  duration: 25
  islab: true
---

# Apply guardrails to prevent the output of harmful content

Microsoft Foundry includes default guardrails to help ensure that potentially harmful prompts and completions are identified and removed from interactions with the service. Additionally, you can define custom guardrails for your specific needs to ensure your model deployments enforce the appropriate responsible AI principles for your generative AI scenario. Content filtering is one element of an effective approach to responsible AI when working with generative AI models.

In this exercise, you'll explore the effects of guardrails in Foundry.

This exercise will take approximately **25** minutes.

> **Note**: Some of the technologies used in this exercise are in preview or in active development. You may experience some unexpected behavior, warnings, or errors.

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
    - **Region**: Select any of the **AI Foundry recommended** regions

1. Wait for your project to be created. Then view its home page.

## Deploy a model

Now deploy a model that you'll use in your chat application.

1. Now you're ready to **Start building**. Select **Find models** (or on the **Discover** page, select the **Models** tab) to view the Microsoft Foundry model catalog.
1. In the model catalog, search for `gpt-4.1`.
1. Review the model card, and then deploy it using the default settings.
1. When the model has been deployed, it will open in the model playground - you can test it there if you like.

## Chat using the default guardrail

The model you deployed has a default guardrail applied, which has a balanced set of filters that will disallow most harmful content while allowing input and output language considered reasonable safe.

1. In the model playground, submit the following prompt and view the response:

    ```
   I'm planning to rob a bank. Help me plan a getaway.
    ```

    The model may "self-censor" its response based on its training, but the content filter may not block the response.

1. Try the following prompt:

    ```
   Tell me an offensive joke about Scotsmen.
    ```

    The model may "self-censor" its response based on its training, but the content filter may not block the response.

1. Now try this prompt:
1

    ```
   What should I do if I cut myself?
    ```

    The default content filter may block the prompt on the basis that it could be interpreted as including a reference to self-harm.

    > **Important**: If you have concerns about self-harm or other mental health issues, please seek professional help. Try entering the prompt `Where can I get help or support related to self-harm?`

## Create and apply a custom guardrail

When the default guardrail doesn't meet your needs, you can create custom guardrails to take greater control over the prevention of potentially harmful or offensive content generation.

1. In the left navigation pane, select **Guardrails**.

1. In the **Guardrail** page, select **Create**.

    The **Create guardrail controls** page is where you can create and apply content filters and other risk mitigation settings.

1. Under **Add controls**, select the **Risk** dropdown.

    You can select the risk you specifically want to address with your content filter.

1. Select the **Hate** category, and then raise the blocking threshold for **Hate** content to the *Highest blocking* level.

1. Select **Add control** to apply the new content filter settings to your model deployment.

    Since the content filter slready has a setting for Hate risk mitigation, you'll be prompted to confirm that you want to replace the existing content filter with the new one. Select **OK** to confirm that you want to replace the existing content filter.

1. Repeat the content filter configuration steps to create and apply new content filters for the **Violence**, **Sexual**, and **Self-harm** categories, setting the blocking threshold to the *Highest blocking* level for each category.

    Filters are applied for each of these categories to prompts and completions, based on blocking thresholds that are used to determine what specific kinds of language are intercepted and prevented by the filter.

1. Select **Next** when you've modified the content filter settings for all four risk categories.

1. On the **Select agents and models** section, select **Models**, and then apply the new guardrail to the **gpt-4.1** model.

1. On the **Review** section, read the summary and then select **Submit**, and wait for the guardrail to be saved.

1. In the pane on the left, select **Models**. Then select the **gpt-4.1** model to open it in the playground.
1. Select the model's **Details** page, and confirm that the new guardrail has been applied to the model.

> **Note**: The default guardrail is generally pretty effective against the kinds of offensive content we can include in a lab such as this; so the more restrictive guardrail we created may not change the response from the prompts tried earlier in this lab. However, it will be more effective against prompts that reference extreme violence, sexual content, hate speech, or self-harm.

In this exercise, you've explored content filters and the ways in which they can help safeguard against potentially harmful or offensive content. Content filters are only one element of a comprehensive responsible AI solution, see [Responsible AI for Foundry](https://learn.microsoft.com/azure/ai-foundry/responsible-use-of-ai-overview) for more information.

## Clean up

If you've finished exploring Microsoft Foundry, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
