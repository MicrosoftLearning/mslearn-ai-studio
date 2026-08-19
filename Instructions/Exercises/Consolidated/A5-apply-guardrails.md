---
lab:
    title: 'Task 5 – Apply guardrails to block harmful content'
    description: 'Explore the default guardrail on your model deployment, then create and apply a stricter custom guardrail for the Wingtip Journeys assistant.'
    level: 300
    concepts: 'guardrails, content filters, responsible AI, blocking thresholds'
    islab: true
    status: 'draft'
---

# Task 5 — Apply guardrails to block harmful content

*Part of the **Choose, evaluate, and safeguard a model** lab. New here? Start with [Getting started](A0-getting-started.md).*

> **What you need:** a **Microsoft Foundry project with a `gpt-5.2` deployment**. Don't have
> one? Complete [Getting started](A0-getting-started.md) first — its *Deploy a model* section
> is all you need. This task is completed entirely in the portal, and nothing from Tasks 1–4
> carries over beyond that deployment.

> **Continuing from a previous task?** If you just finished
> [Task 4](A4-evaluate-a-model.md), the `gpt-5.2` deployment you evaluated is the same one you
> safeguard here — go straight to *Chat using the default guardrail*.

---

Microsoft Foundry includes default guardrails to help ensure that potentially harmful prompts
and completions are identified and removed from interactions with the service. Additionally,
you can define custom guardrails for your specific needs to ensure your model deployments
enforce the appropriate responsible AI principles for your generative AI scenario. Content
filtering is one element of an effective approach to responsible AI when working with
generative AI models.

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
<summary>Self-censoring vs. filtering — what's the difference?</summary>
<div class="concept-body" markdown="1">

When a model declines a request because of its own training, that's **alignment**. It's
helpful, but it's a property of the model and it varies by prompt, by phrasing, and by model
version.

A **guardrail** is a separate service that inspects both the prompt and the completion and
blocks them against thresholds *you* configure. It's deterministic, it's auditable, and it
survives a model swap. For a consumer brand like Wingtip Journeys, that difference is the
whole point: you can't put "the model usually refuses" in a compliance document.

</div>
</details>

## Chat using the default guardrail

The model you deployed has a default guardrail applied, which has a balanced set of filters that will disallow most harmful content while allowing input and output language considered reasonably safe.

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

    Since the content filter already has a setting for Hate risk mitigation, you'll be prompted to confirm that you want to replace the existing content filter with the new one. Select **OK** to confirm that you want to replace the existing content filter.

1. Repeat the content filter configuration steps to create and apply new content filters for the **Violence**, **Sexual**, and **Self-harm** categories, setting the blocking threshold to the *Highest blocking* level for each category.

    Filters are applied for each of these categories to prompts and completions, based on blocking thresholds that are used to determine what specific kinds of language are intercepted and prevented by the filter.

1. Select **Next** when you've modified the content filter settings for all four risk categories.

1. On the **Select agents and models** section, select **Models**, and then apply the new guardrail to the **gpt-5.2** model.

1. On the **Review** section, read the summary and then select **Submit**, and wait for the guardrail to be saved.

1. In the pane on the left, select **Deployments**. Then select the **gpt-5.2** model to open it in the playground.
1. Select the model's **Details** page, and confirm that the new guardrail has been applied to the model.

> **Note**: The default guardrail is generally pretty effective against the kinds of offensive content we can include in a lab such as this; so the more restrictive guardrail we created may not change the response from the prompts tried earlier in this lab. However, it will be more effective against prompts that reference extreme violence, sexual content, hate speech, or self-harm.

> ✅ **Checkpoint**: The Wingtip Journeys model deployment is protected by a custom guardrail
> whose thresholds you chose, rather than by the model's own judgment alone.

Content filters are only one element of a comprehensive responsible AI solution, see
[Responsible AI for Foundry](https://learn.microsoft.com/azure/ai-foundry/responsible-use-of-ai-overview)
for more information.

---

**Next (optional):** [Task 6 — Fine-tune a model for a consistent voice](A6-fine-tune-a-model.md)
