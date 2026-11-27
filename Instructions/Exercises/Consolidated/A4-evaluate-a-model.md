---
lab:
    title: 'Task 4 – Evaluate a model with a synthetic dataset'
    description: 'Run a repeatable evaluation of your model against a synthetically generated set of Wingtip Journeys traveler questions, then analyze the failures.'
    level: 300
    concepts: 'model evaluation, synthetic data generation, AI-assisted evaluators'
    islab: true
    status: 'draft'
---

# Task 4 — Evaluate a model with a synthetic dataset

*Part of the **Choose, evaluate, and safeguard a model** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project with a `gpt-5.2` deployment**. Don't have
> one? Complete [Getting started](A0-getting-started.md) first — its *Deploy a model* section
> gets you there in a couple of minutes. This task is completed entirely in the portal; you
> don't need anything from Tasks 1–3 beyond that deployment, and no local code or
> configuration is required.

> **Continuing from a previous task?** If you just finished
> [Task 2](A2-compare-models.md) you have both `gpt-5.2` and `gpt-5-mini` deployed. This task
> evaluates `gpt-5.2` — keep `gpt-5-mini` around, because re-running the same evaluation
> against it is the stretch goal at the end.

---

The model playground is useful for quick manual testing, but to systematically assess a
model's performance across many inputs, you run an **evaluation**. Let's evaluate the
**gpt-5.2** model using a synthetically generated dataset of Wingtip Journeys traveler
questions.

<style>
/* "Ask Wren" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
  font-size:.85em; font-weight:600; color:#0f6cbd; background:#0f6cbd12;
  border:1px solid #0f6cbd33; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Wren: "; font-weight:700; }
details.concept > summary:hover { background:#0f6cbd; color:#fff; border-color:#0f6cbd; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #0f6cbd33; border-top:none;
  border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#0f6cbd08; font-size:.95em; }
</style>

<details markdown="1" class="concept">
<summary>A model judging a model — really?</summary>
<div class="concept-body" markdown="1">

Yes, and it's more defensible than it sounds. The evaluators you'll enable are
*AI-assisted*: a judge model scores each response against a specific rubric — is it relevant,
is it coherent, is it grounded in the input. Scoring thousands of free-text answers by hand
isn't feasible, and keyword matching can't tell "helpful" from "wrong but confident".

The important discipline is the same as with human raters: look at the failures, not just the
average. That's what the **Analyze results** step at the end of this task is for.

</div>
</details>

## Run an evaluation

### Step 1: Target

1. In the playground, select the **Evaluations** tab.
1. Select **Create** to open the **Create new evaluation** wizard.
1. For the evaluation target, select **Model**.
1. In the table of models, deselect any preselected deployments so that only the checkbox for **gpt-5.2** is selected, and then select **Next**.

### Step 2: Data

Instead of uploading a test dataset, you'll use Foundry's synthetic data generation feature to create one automatically.

1. In the **Data** step, under **Dataset source**, select **Synthetic generation**.

    With synthetic generation, a deployment is used to automatically generate questions for each target when you submit the evaluation.

1. Select **Generate**, and then set and confirm the following:
    - **Name of the new dataset**: *Leave as default*
    - **Model**: gpt-5.2
    - **Number of rows**: 45
    - **Prompt**: `Create various travel related questions a Wingtip Journeys customer might ask, and include some content safety and security tests`
    - **Seed data**: *Leave blank*
1. Select **Next** to proceed.

### Step 3: Configure models

1. In the **Configure models** step, set the **Developer** prompt for the model being evaluated:

    ```
    You are the Wingtip Journeys travel assistant. You provide accurate, detailed, and practical travel advice to help customers plan their trips.
    ```

1. Leave the rest of the values at their default, then select **Next**.

### Step 4: Criteria

1. In the **Criteria** step, view all of the suggested evaluators. These use an AI model as a judge to assess the quality of responses.
1. Remove all of the criteria under *Agents* and *Safety*, leaving the rest of the evaluators enabled.
1. Select **Next**.

### Step 5: Review and submit

1. In the **Review** step, verify the evaluation configuration, including the target model, dataset, and selected criteria.
1. Provide a name for the evaluation, such as `wingtip-assistant-eval`.
1. Select **Submit** to start the evaluation run.
1. Wait for the evaluation to complete. This may take several minutes, depending on data center load.

## Review the results

1. When the evaluation completes, select the evaluation run to view the results page, which displays an overview of the evaluation metrics.
1. Review the scores and results from each evaluation in the table detailed on the run page. Scroll to the right and view additional pages, where you'll see mostly passing values. Depending on the model's response, you may see some failures. If you do, examine those closely.
1. Select the **Analyze results** button, selecting **gpt-5.2** from the dropdown, then select **Start analysis**.
1. On this page you'll see any failures clustered by why they failed, where you can see details on why it failed. Most of those failures will be due to the model saying it's unable to help due to the nature of the question, however you should explore each failure and consider if the response is what you want to see.
1. Review any failures and the AI suggestions for how to improve. This guidance will help you tweak your configuration to perform better.

> ✅ **Checkpoint**: You've produced a repeatable, scored measurement of how the model handles
> Wingtip Journeys traveler questions — and you've inspected the cases where it fell short.

**Stretch**: run the same evaluation against the **gpt-5-mini** deployment from
[Task 2](A2-compare-models.md) and compare the two runs. Does the cheaper model lose enough
quality to matter for Wingtip Journeys?

---

**Next (optional):** [Task 5 — Apply guardrails to block harmful content](A5-apply-guardrails.md)
