---
lab:
  title: Explore and compare models
  description: Explore the model catalog to find and compare models, and evaluate model performance.
  level: 300
  duration: 45
  islab: true
---

# Explore and compare models

The Microsoft Foundry model catalog serves as a central repository where you can explore and use a variety of models, facilitating the creation of your generative AI scenario. In this exercise, you'll explore the model catalog, compare models using benchmarks, test models in the model playground, and run an evaluation using a synthetic dataset.

This exercise will take approximately **45** minutes.

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

## Explore models in the catalog

Microsoft Foundry Models provides a catalog of models that you can use in your project. You can browse the catalog and compare models to find the right one for your needs.

1. Now you're ready to **Start building**. Select **Find models** (or on the **Discover** page, select the **Models** tab) to view the Microsoft Foundry model catalog.

    The model catalog lists all models available in Foundry. Some are provided directly from Azure (and billed through your Azure subscription) while others are provided by partners and the community.

    Note that you can search and filter the catalog, based on model names, capabilities, and other factors.

1. Search for `gpt-4.1`. Then, in the search results, select the **gpt-4.1** model to view its *model card*. Model cards provide information about models to help you determine if they are suitable for your needs.
1. Read the description and review the other information available on the **Details** page.
1. View the **Benchmarks** page for the gpt-4.1 model to see how the model compares across some standard performance benchmarks with other models that are used in similar scenarios.
1. Use the back arrow (**&larr;**) next to the **gpt-4.1** page title to return to the model catalog.

## Compare models using the model leaderboard

Now let's use the model leaderboard and side-by-side comparison features to compare models visually.

1. In the model catalog page, select **View leaderboard**.
1. In the **Model leaderboard** page, review the top models ranked by quality, safety, cost, and performance. Note which models score highest for AI quality metrics.
1. Scroll down to use the **Trade-off chart** section to compare models on multiple dimensions.
1. Select the **Estimated cost** from the dropdown to see how model quality relates to estimated cost, and then use the model list to select only the **gpt-4.1**, **gpt-4.1-mini**, and **gpt-4.1-nano** models to compare them.
1. Select the **Throughput** metric from the dropdown to see how the quality of these models relates to throughput scores.
1. Select the **Safety** metric from the dropdown to see how the quality of these models relates to safety scores.
1. In the table just above the trade-off charts, you can compare benchmarks. Select the **gpt-4.1**, **gpt-4.1-mini**, and **gpt-4.1-nano** models, and then use the **Compare models** button to view their benchmarks side-by-side.
1. Select **Compare models** to open the side-by-side comparison view.
1. Review the comparison across the following data:
    - **Performance benchmarks**: Quality, safety, and throughput scores.
    - **Input** and **output**: The formats supported for prompts and responses.
    - **Context**: The number of tokens that can be maintained in a conversation and produced as output, and when the model was trained.
    - **Endpoints**: The API endpoints through which the model can be consumed by client applications, and whether it can be used by an agent.
    - **Supported features**: Specific capabilities that you may require in your application scenario.
1. Use the back arrow (**&larr;**) next to the **gpt-4.1** page title to return to the model catalog.

## Deploy models

Now let's deploy the models we'll use for testing and evaluation. You need to deploy **gpt-4.1** and **gpt-4o-mini**.

### Deploy the gpt-4.1 model

1. In the model catalog, search for `gpt-4.1` and select it.
1. On the model page, select **Deploy** and deploy the model using the *default settings.

    The deployed model will open in the model playground, where it will be selected in the **Model** drop-down list.

1. Note the deployment name (for example, **gpt-4.1**).

### Deploy the gpt-4o-mini model

1. In the model playground, in the **Model** list, select **Browse more models**.
1. Search for `gpt-4o-mini`, and then select it and deploy it.

    The model is deployed and selected in the model playground.

1. Note the deployment name (for example, **gpt-4o-mini**).

## Compare models in the model playground

Now that you have two model deployments, let's compare them in the playground.

1. In the playground, ensure the **gpt-4.1-mini** model is selected in the **Models** list, and then on the right side of the page, in the **Compare models** list, select the **gpt-4.1** model.
1. Select the **Setup** tabs for both models, and set the **Instructions** to `You are an AI assistant that helps solve problems.`
1. Select the **Chat** tabs for both models, and enter the following prompt:

    ```
   I have a fox, a chicken, and a bag of grain that I need to take over a river in a boat. I can only take one thing at a time. If I leave the chicken and the grain unattended, the chicken will eat the grain. If I leave the fox and the chicken unattended, the fox will eat the chicken. How can I get all three things across the river without anything being eaten?
    ```

1. Submit the prompt and view the responses from both models. Then, enter the following follow-up prompt:

    ```
   Explain your reasoning.
    ```

1. Compare the responses from each model. Note any differences in accuracy, reasoning quality, and response style.

## Evaluate a model with a synthetic dataset

The model playground is useful for quick manual testing, but to systematically assess a model's performance across many inputs, you can run an evaluation. Let's evaluate the **gpt-4.1** model using a synthetically generated dataset of travel-related questions.

### Step 1: Target

1. In the playground, select the **Evaluations** tab.
1. Select **Create** to open the **Create new evaluation** wizard.
1. For the evaluation target, select **Model**.
1. Select just your **gpt-4.1** deployment in the table of models, and then select **Next**.

### Step 2: Data

Instead of uploading a test dataset, you'll use Foundry's synthetic data generation feature to create one automatically.

1. In the **Data** step, under **Dataset source**, select **Synthetic generation**.

    With synthetic generation, a deployment is used to automatically generate questions for each target when you submit the evaluation.

1. Select **Generate**, and then set and confirm the following:
    - **Name of the new dataset**: *Leave as default*
    - **Model**: gpt-4.1
    - **Number of rows**: 45
    - **Prompt**: `Create various travel related questions, and include some content safety and security tests`
    - **Seed data**: *Leave blank*
1. Select **Next** to proceed.

### Step 3: Configure models

1. In the **Configure models** step, set the **Developer** prompt for the model being evaluated:

    ```
    You are a helpful travel assistant that provides accurate, detailed, and practical travel advice to help users plan their trips.
    ```

1. Leave the rest of the values at their default, then select **Next**.

### Step 4: Criteria

1. In the **Criteria** step, all of the suggested evaluators. These use an AI model as a judge to assess the quality of responses.
1. Remove all of the criteria under *Agents*, leaving the rest of the evaluators enabled.
1. Select **Next**.

### Step 5: Review and submit

1. In the **Review** step, verify the evaluation configuration, including the target model, dataset, and selected criteria.
1. Provide a name for the evaluation, such as `travel-assistant-eval`.
1. Select **Submit** to start the evaluation run.
1. Wait for the evaluation to complete. This may take several minutes, depending on data center load.

### Review the results

1. When the evaluation completes, select the evaluation run to view the results page displays an overview of the evaluation metrics.
1. Review the scores and results from each evaluation in the table detailed on the run page. Scroll to the right and view additional pages, where you'll see mostly passing values. Depending on the model's response, you may see some failures. If you do, examine those closely.
1. Select the **Analyze results** button, selecting **gpt-4.1** from dropdown, then select **Start analysis**.
1. On this page you'll see any failures clustered by why they failed, where you can see details on why it failed. Most of those failures will be due to the model saying it's unable to help due to the nature of the question, however you should explore each failure and consider if the response is what you want to see.
1. Review any failures and the AI suggestions for how to improve. This guidance will help you tweak your configuration to perform better.

## Clean up

If you've finished exploring Microsoft Foundry, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Open the [Azure portal](https://portal.azure.com) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
