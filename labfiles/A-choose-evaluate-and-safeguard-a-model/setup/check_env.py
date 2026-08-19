"""
Preflight check for the Wingtip Journeys "Choose, evaluate, and safeguard a model" lab.

WORKING DIRECTORY: run this from the lab folder --
    labfiles/A-choose-evaluate-and-safeguard-a-model
so the path below is "setup/check_env.py". Unlike the companion chat-app lab,
this lab has no python/ code folder and no virtual environment: the script uses
only the Python standard library, so it runs on a clean Python install.

Each task in this lab can be completed on its own. Before you start a task, run this
script to confirm you have what that task needs:

    cd labfiles/A-choose-evaluate-and-safeguard-a-model
    python setup/check_env.py --task 6

Every task in this lab is completed in the Microsoft Foundry portal, so there is no
.env file and nothing to install. The check therefore does two things: it reminds you
of the portal prerequisites for the task you picked, and it verifies that any local
data files that task uses are present and valid.

It never changes anything and never calls Azure.

Tasks and what they need:

    Task 1  (portal)  an Azure subscription with quota for Azure AI resources
    Task 2  (portal)  a Foundry project
    Task 3  (portal)  a Foundry project with a deployed model, plus VS Code
    Task 4  (portal)  a Foundry project with a gpt-5.2 deployment
    Task 5  (portal)  a Foundry project with a gpt-5.2 deployment
    Task 6  (portal)  a Foundry project in a fine-tuning region, plus the local
                      training dataset in data/
"""

import argparse
import json
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = LAB_ROOT / "data"

TRAIN_FILE = "wingtip-finetune-train.jsonl"
VALIDATION_FILE = "wingtip-finetune-validation.jsonl"

# What each task expects you to have set up in the Foundry portal.
PORTAL_REQUIREMENTS = {
    1: [
        "An Azure subscription with permission and quota to create Azure AI resources.",
    ],
    2: [
        "A Microsoft Foundry project (Task 2 deploys the models it compares).",
    ],
    3: [
        "A Microsoft Foundry project with a deployed model.",
        "Visual Studio Code installed locally.",
    ],
    4: [
        "A Microsoft Foundry project with a gpt-5.2 deployment.",
    ],
    5: [
        "A Microsoft Foundry project with a gpt-5.2 deployment.",
    ],
    6: [
        "A Microsoft Foundry project in a region that supports fine-tuning",
        "  (at the time of writing: North Central US or Sweden Central).",
        "A gpt-4.1 deployment to use as the fine-tuning base and baseline.",
    ],
}

# Local data files each task uses, if any.
DATA_REQUIREMENTS = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [TRAIN_FILE, VALIDATION_FILE],
}


def check_jsonl(path):
    """Return (ok, detail) for a chat-format JSONL training file."""
    if not path.exists():
        return False, "not found"

    line_count = 0
    # utf-8-sig so a BOM (added by some editors when re-saving the downloaded
    # dataset) is consumed instead of making line 1 fail to parse as JSON.
    try:
        handle = path.open(encoding="utf-8-sig")
    except OSError as error:
        return False, f"could not be read ({error.strerror or error})"

    with handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                return False, f"line {line_number} is not valid JSON ({error.msg})"
            messages = record.get("messages")
            if not isinstance(messages, list) or not messages:
                return False, f"line {line_number} has no 'messages' list"
            roles = {message.get("role") for message in messages}
            if not {"system", "user", "assistant"} <= roles:
                return False, f"line {line_number} is missing a system, user, or assistant message"
            line_count += 1

    if line_count == 0:
        return False, "file is empty"
    return True, f"{line_count} valid training examples"


def main():
    parser = argparse.ArgumentParser(
        description="Check that you're ready to start a task in this lab."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=sorted(PORTAL_REQUIREMENTS),
        required=True,
        help="Which task you're about to start (1-6).",
    )
    args = parser.parse_args()

    print(f"Checking readiness for Task {args.task}")
    print(f"Lab folder: {LAB_ROOT}")
    print()

    print("This task is completed in the Microsoft Foundry portal. You'll need:")
    for requirement in PORTAL_REQUIREMENTS[args.task]:
        print(f"  - {requirement}")
    print()

    required_files = DATA_REQUIREMENTS[args.task]
    if not required_files:
        print("No local files are needed for this task.")
        print("Nothing else to check - head to the task page.")
        return 0

    print("Local data files this task uses:")
    problems = []
    for file_name in required_files:
        path = DATA_DIR / file_name
        ok, detail = check_jsonl(path)
        mark = "OK " if ok else "PROBLEM"
        print(f"  [{mark}] data/{file_name} - {detail}")
        if not ok:
            problems.append(file_name)

    print()
    if problems:
        print("Fix the following before starting this task:")
        for file_name in problems:
            print(f"\n  data/{file_name}")
            print(
                "    Re-clone the mslearn-ai-studio repo, or download the file from "
                "https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-studio/"
                "main/labfiles/A-choose-evaluate-and-safeguard-a-model/data/" + file_name
            )
        return 1

    print(f"You're ready to start Task {args.task}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
