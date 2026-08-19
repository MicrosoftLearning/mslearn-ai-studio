# Lab B — Solution (complete code)

This folder contains **finished, working versions** of every code file learners write in
*Build a generative AI chat app*. Use it to unblock a stuck learner, verify expected behavior,
or run the whole scenario end to end.

All tasks share a **single** `python/` folder (one virtual environment, one `.env`), exactly
like the starter code learners work in:

```
Solution/
└─ python/
   ├─ chat-app.py       # Tasks 1 & 2 - console chat app (Responses API, context, streaming)
   ├─ chat-async.py     # Task 3 - the same app using the asynchronous API
   ├─ tools-app.py      # Task 4 - chat grounded with file_search + web_search
   ├─ guides/           #   Task 4 grounding data: Wingtip Journeys destination guides
   ├─ .env.example      # configuration template (no secrets)
   └─ requirements.txt  # pinned to the same packages as the starter folder
```

`chat-app.py` is shown here in its **final** state — the streaming version produced at the end
of Task 2. Tasks 1 and 2 build it up in stages (Chat Completions → Responses → conversation
tracking → streaming), and each stage's code appears in the corresponding instruction page's
*Show a solution* block.

---

## Setup helpers and modular (per-task) labs

This lab can be completed end to end **or one task at a time**. Two things make that possible:

- **Per-task instruction pages** —
  `Instructions/Exercises/Consolidated/B0-getting-started.md` (shared setup) plus `B1`–`B4`
  (one page per task). Each task page tells a standalone learner exactly what it needs.
- **A setup script** in `labfiles/B-build-a-generative-ai-chat-app/setup/`:
  - `check_env.py --task N` — preflight-checks that `.env` has the keys task *N* needs, and
    (for Task 4) that the `guides/` folder is present. Run it from the **starter**
    `labfiles/B-build-a-generative-ai-chat-app/python/` folder (**not** `Solution/python/`) as
    `python ../setup/check_env.py --task N`.

The script is run from the **starter** `python/` folder and uses the shared virtual environment
and `.env`. There is no `setup/` folder inside `Solution/`, so `../setup/...` only resolves
from the starter tree.

---

## What YOU must do to run this solution (the agent can't do these for you)

Everything below requires an Azure subscription and interactive sign-in, so it can't be
automated in the repo. Do these once, then run each task.

### 1. Microsoft Foundry setup
1. Have an **Azure subscription** with access to **Microsoft Foundry**.
2. Create (or open) a **Foundry project**.
3. **Deploy a model** (for example `gpt-5.2`) in that project and note the **deployment name**.
4. Copy the **Azure OpenAI endpoint** from the project home page — *not* the project endpoint.
5. Make sure your signed-in identity has the **Azure AI User** role (or equivalent) on the project.

The companion lab,
[Choose, evaluate, and safeguard a model](../../../Instructions/Exercises/Consolidated/A-choose-evaluate-and-safeguard-a-model.md),
walks through steps 1–4 in detail.

### 2. Set up the environment once (shared by all tasks)
From `Solution/python/` (or the starter `python/` folder if you're running the learner's copy):
```
python -m venv labenv
.\labenv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
```
Then copy `.env.example` to `.env` and fill in the values (all tasks read the same file):
- `AZURE_OPENAI_ENDPOINT` — the **Azure OpenAI endpoint**, used by every task
- `MODEL_DEPLOYMENT` — your model deployment name, used by every task

### 3. Sign in locally
```
az login
```
Sign in with the same account that has access to the project. A missing or expired `az login`
is the most common cause of an authentication error on the first prompt.

### 4. Run each task
All commands run from the single `Solution/python/` folder:

| Task | Command | What you get |
|------|---------|--------------|
| 1 | `python chat-app.py` | Console chat with the model, one turn at a time |
| 2 | `python chat-app.py` | The same app, now with conversation context and streamed output |
| 3 | `python chat-async.py` | The same conversation using the asynchronous API |
| 4 | `python tools-app.py` | Chat grounded in the Wingtip Journeys guides, plus live web search |

Enter `quit` at any prompt to exit an app.

Task 4 creates a **vector store** in your Foundry project each time it runs and uploads the
five Markdown files in `guides/`. Vector stores persist, so delete the resource group when
you're finished with the lab.

---

## Quick sanity checks that DON'T need Azure

> In this section, `Solution/python/` means the folder this README sits next to. The one
> command that reaches outside it is called out explicitly, because `Solution/` has no
> `setup/` folder of its own.

- From `Solution/python/`: `python -m py_compile chat-app.py chat-async.py tools-app.py` — all
  solution files compile.
- From `Solution/python/`: `python -c "import glob; print(len(glob.glob('guides/*.md')))"`
  should print **5** — the number of guides Task 4 uploads.
- From the **starter** `python/` folder (**not** `Solution/python/`):
  `python ../setup/check_env.py --help` runs cleanly with no network access, and works even
  before you `pip install -r requirements.txt`.
