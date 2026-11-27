# Lab A — Choose, evaluate, and safeguard a model (lab files)

Supporting files for the consolidated lab
[**Choose, evaluate, and safeguard a model**](../../Instructions/Exercises/Consolidated/A-choose-evaluate-and-safeguard-a-model.md).

Every task in this lab is completed in the **Microsoft Foundry portal**, so there is no
application code to write and no virtual environment to create. The lab ships only the
assets the portal tasks consume, plus a preflight script.

```
A-choose-evaluate-and-safeguard-a-model/
├─ data/
│  ├─ wingtip-finetune-train.jsonl        # Task 6 - supervised fine-tuning training data
│  └─ wingtip-finetune-validation.jsonl   # Task 6 - optional validation data (stretch goal)
└─ setup/
   └─ check_env.py                        # per-task readiness check (no Azure calls)
```

## The datasets

Both files use the chat completion JSONL format that supervised fine-tuning expects: one JSON
object per line, each with a `messages` array containing a `system`, `user`, and `assistant`
message.

Every example shares the same system message — the Wingtip Journeys house prompt — and models
the house voice: warm, playful, and always closing with a question. Crucially, no example
recommends a hotel, flight, rental car, or restaurant, because that's the behavior the
fine-tune is meant to suppress.

## Running the readiness check

From this folder:

```
python setup/check_env.py --task 6
```

Swap `6` for the task you're about to start (1-6). The script reads local files only, never
calls Azure, and never changes anything. `--help` lists the valid range.

It needs no packages beyond the Python standard library, so it runs on a clean Python 3.13
install.

## What YOU must do (the files can't do it for you)

1. Have an **Azure subscription** with permission and quota to create Azure AI resources.
2. Create a **Microsoft Foundry project** — see
   [Getting started](../../Instructions/Exercises/Consolidated/A0-getting-started.md).
3. For **Task 6**, create that project in **North Central US** or **Sweden Central**, and deploy
   **gpt-4.1** as the fine-tuning base model.
4. Delete the resource group when you're finished. A fine-tuned model deployment keeps
   incurring hosting charges until it's removed.

## Quick sanity checks that don't need Azure

- `python setup/check_env.py --task 6` — validates both JSONL files parse and are well formed.
- `python setup/check_env.py --help` — runs cleanly with no network access.
