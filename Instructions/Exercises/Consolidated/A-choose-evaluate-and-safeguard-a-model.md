---
lab:
    title: 'Choose, evaluate, and safeguard a model'
    description: 'Pick the right model for the Wingtip Journeys travel assistant: create a Foundry project, compare models in the catalog and playground, evaluate one systematically, apply guardrails, and fine-tune it for a consistent voice. A modular lab you can complete end to end or one task at a time.'
    level: 300
    concepts: 'model catalog, model comparison, evaluation, guardrails, fine-tuning'
    duration: 35
    islab: true
    status: 'draft'
---

<!--
CONSOLIDATION NOTE (remove before publishing):
"Lab A" consolidates the source exercises 01 (Prepare for an AI development project),
02 (Explore and compare models), 06 (Apply guardrails), and 04b (Fine-tune a language model)
into one modular lab with a Core + Optional task flow.

Every task is completed in the Microsoft Foundry portal, so there is no application code
to write. The only assets the lab ships are the fine-tuning datasets and a preflight script,
in labfiles/A-choose-evaluate-and-safeguard-a-model/.

This landing page is the lab overview. Setup lives in A0-getting-started.md and each task is
its own page (A1-A6) so it can be completed on its own.
-->

# Choose, evaluate, and safeguard a model

**Difficulty** ▰▰▰▱▱ **L300**  (filled bars out of 5; **L100** beginner → **L500** expert)

Before you write a single line of application code, you have to answer three questions:
*which model?*, *is it good enough?*, and *is it safe to ship?* In this lab you'll answer all
three in the Microsoft Foundry portal.

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
<summary>Why does model choice matter so much?</summary>
<div class="concept-body" markdown="1">

Every generative AI solution rests on at least one model, and models differ enormously in
quality, cost, latency, context size, and the tools they support. Picking one is a trade-off,
not a ranking — the "best" model is the cheapest one that is still good enough for *your*
scenario. That's why Foundry gives you a catalog, benchmarks, a leaderboard, a side-by-side
playground, and a repeatable evaluation harness: so the choice is evidence-based.

</div>
</details>

**Your scenario:** you're the AI developer at **Wingtip Journeys**, a travel company that
plans small-group trips. Wingtip Journeys wants an AI travel assistant that inspires
travelers, answers destination questions accurately, keeps a warm and consistent house
voice, and never produces content that would embarrass the brand. Across this lab you'll
choose the model that powers it — and prove it's the right one.

You'll start with the **Core** tasks that get you to a deployed, tested model as quickly as
possible. From there, a set of **Optional** tasks lets you go deeper into the areas that
interest you most.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** tasks of this exercise, you'll be able to:

- **Create a Microsoft Foundry project** and deploy a model, then find the endpoints that
  client applications use to connect to it.
- **Compare models** using model cards, benchmarks, the model leaderboard, and a
  side-by-side playground comparison.

The **Optional** tasks let you additionally:

- Work with your project from **Visual Studio Code** using the Foundry Toolkit extension.
- **Evaluate a model systematically** against a synthetically generated dataset.
- **Apply guardrails** that block harmful prompts and completions.
- **Fine-tune a model** on your own training data so it answers in a consistent house voice.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** —
so you can pick a single task and do just that one. Every task uses the same Foundry project,
so if you'd rather work straight through, you can.

1. **Start with [Getting started](A0-getting-started.md)** — create your Microsoft Foundry
   project and deploy the model the rest of the lab builds on. Every task begins here; if
   you're doing the whole lab in one sitting, you only need to do this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** tasks first (about **35 minutes**) — they end with a deployed model you
have compared against a credible alternative. Then expand any **Optional** tasks that
interest you. The full lab, including all optional tasks, takes about **3 hours 5 minutes**
(most of that is waiting for the fine-tuning job in Task 6).

| Section | Task | Difficulty | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Create a project and deploy a model](A1-create-a-project-and-deploy-a-model.md) | ▰▰▱▱▱ L200 | ~15 min |
| **Core** | [Task 2 – Compare models in the catalog and playground](A2-compare-models.md) | ▰▰▱▱▱ L200 | ~20 min |
| *Optional* | [Task 3 – Explore your project from Visual Studio Code](A3-explore-your-project-from-vs-code.md) | ▰▰▱▱▱ L200 | ~10 min |
| *Optional* | [Task 4 – Evaluate a model with a synthetic dataset](A4-evaluate-a-model.md) | ▰▰▰▱▱ L300 | ~25 min |
| *Optional* | [Task 5 – Apply guardrails to block harmful content](A5-apply-guardrails.md) | ▰▰▰▱▱ L300 | ~25 min |
| *Optional* | [Task 6 – Fine-tune a model for a consistent voice](A6-fine-tune-a-model.md) | ▰▰▰▰▱ L400 | ~90 min |

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~35 min):** do Tasks 1–2.
- **Core + recommended (~1h 25m):** also do **Task 4** (evaluation) and **Task 5** (guardrails).
- **Everything (~3h 5m):** add **Task 3** (VS Code) and **Task 6** (fine-tuning). Task 6 is
  mostly waiting, so start its job early and do the other tasks while it runs.

> **One project, one assistant**: every task in this lab works against the same Foundry
> project and the same Wingtip Journeys travel assistant persona. Each task judges that
> assistant from a different angle — capability, quality, safety, and voice.

## Where this lab leads

This lab stops at the portal: you finish with a model you've chosen, measured, safeguarded,
and (optionally) tuned. The companion lab
**[Build a generative AI chat app](B-build-a-generative-ai-chat-app.md)** picks up from there
and puts that model behind an application you write in Python.

## Summary

Across this lab you:

- Created a **Microsoft Foundry project**, deployed a model, and located the resource and
  project endpoints client applications use.
- **Compared models** with model cards, benchmarks, the leaderboard trade-off charts, and a
  side-by-side playground comparison.
- (Optionally) explored your project from **Visual Studio Code**, **evaluated** a model against
  a synthetic dataset, applied **guardrails** to block harmful content, and **fine-tuned** a
  model so it answers in the Wingtip Journeys house voice.

Together these are the evidence you need to defend a model choice to your team: what it can
do, how well it does it, how safely, and how consistently.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> Deleting the resource group removes the project, every model deployment, any guardrails you
> created, and any fine-tuned model and its deployment. Fine-tuned model deployments continue
> to incur hosting charges until they're deleted, so don't skip this step if you completed
> Task 6.
