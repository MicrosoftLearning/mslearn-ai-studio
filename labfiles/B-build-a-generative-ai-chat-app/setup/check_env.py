"""
Preflight check for the Wingtip Journeys "Build a generative AI chat app" lab.

WORKING DIRECTORY: run this from the STARTER code folder --
    labfiles/B-build-a-generative-ai-chat-app/python
which is the folder you opened a terminal in and created your virtual
environment in. From there the script is one level up, so the path is
"../setup/check_env.py". There is no setup/ folder inside Solution/, so
this does NOT work from Solution/python.

Each task in this lab can be completed on its own. Before you start a task,
run this script to confirm your .env file has everything that task needs:

    cd labfiles/B-build-a-generative-ai-chat-app/python
    python ../setup/check_env.py --task 2

It never changes anything - it only reads your .env (and, for Task 4, the local
destination guides) and tells you what is missing, so you can fix it before
running the task.

Tasks and what they need:

    Task 1  (code)  AZURE_OPENAI_ENDPOINT, MODEL_DEPLOYMENT
    Task 2  (code)  AZURE_OPENAI_ENDPOINT, MODEL_DEPLOYMENT
    Task 3  (code)  AZURE_OPENAI_ENDPOINT, MODEL_DEPLOYMENT
    Task 4  (code)  AZURE_OPENAI_ENDPOINT, MODEL_DEPLOYMENT, plus the guides/ folder
"""

import argparse
import os
from pathlib import Path


def _find_closing_quote(text, quote, start=0, raw=False):
    """Index of the next closing `quote` in `text`.

    By default a backslash-escaped quote does not close the value. This applies
    to BOTH quote characters: dotenv treats \\' inside a single-quoted value as
    an escaped quote, not a terminator. (Note this is asymmetric with decoding,
    where single quotes only ever decode \\' and leave other escapes literal.)

    Pass raw=True to ignore escapes and stop at the very next occurrence of the
    character. dotenv falls back to that behaviour while recovering from a value
    whose quote is never closed, so an escaped quote further down the file still
    terminates the runaway value.
    """
    index = start
    while index < len(text):
        char = text[index]
        if not raw and char == "\\" and index + 1 < len(text):
            index += 2
            continue
        if char == quote:
            return index
        index += 1
    return -1


def _scan_for_close(lines, first_body, quote, next_index):
    """Extend a value line by line until `quote` closes it.

    Returns (body, end, index). `end` is -1 if the quote never closes. Escapes are
    honoured first; if that finds no close anywhere, the scan is retried raw,
    matching dotenv's recovery.
    """
    for raw in (False, True):
        body = first_body
        index = next_index
        end = _find_closing_quote(body, quote, raw=raw)
        while end == -1 and index < len(lines):
            resume = len(body) + 1
            body += "\n" + lines[index]
            index += 1
            end = _find_closing_quote(body, quote, resume, raw=raw)
        if end != -1:
            return body, end, index
    return first_body, -1, next_index


def _decode_single_quoted(value):
    """Decode a single-quoted value the way dotenv does.

    Only the quote and the backslash are escapable: \\' becomes ' and \\\\ becomes
    a single backslash. Everything else stays literal, so '\\n' is a backslash
    followed by n, not a newline.
    """
    return _decode_escapes(value, {"'": "'", "\\": "\\"})


def _decode_double_quoted(value):
    """Apply the backslash escapes dotenv honours inside double quotes."""
    return _decode_escapes(value, {
        "\\": "\\", "'": "'", '"': '"', "a": "\a", "b": "\b",
        "f": "\f", "n": "\n", "r": "\r", "t": "\t", "v": "\v",
    })


def _decode_escapes(value, escapes):
    """Replace known backslash escapes; leave unknown ones (and a trailing
    backslash) exactly as written, which is what dotenv does."""
    out = []
    index = 0
    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value) and value[index + 1] in escapes:
            out.append(escapes[value[index + 1]])
            index += 2
        else:
            out.append(char)
            index += 1
    return "".join(out)


def _parse_env_file(path, problems=None):
    """Minimal .env reader used when python-dotenv isn't importable.

    Matches dotenv.dotenv_values for the syntax a lab .env can contain:

    * blank lines and # comments are skipped
    * an "export " prefix is stripped
    * a key with no "=" maps to None
    * a quoted value keeps any # inside the quotes; an unquoted value drops a
      trailing " #" comment
    * a value opened with a quote may span lines, and the newlines are kept
    * inside double quotes, backslash escapes (\\n, \\", \\\\, ...) are decoded;
      single-quoted values are raw

    Malformed quoting is handled the way dotenv does, which matters because the
    shipped apps use dotenv and so inherit its behaviour exactly:

    * a quote that never closes discards ONLY that binding; parsing resumes on
      the next line, so later settings are still read
    * a quote that closes on a later line but leaves trailing junk discards the
      binding AND everything it swallowed up to that closing quote

    Either way the entry is dropped rather than guessed at, and the line number
    is appended to `problems` so the caller can explain the real cause.

    INTENTIONAL DIVERGENCE FROM DOTENV -- do not "fix" this to match:
    the file is opened utf-8-sig, so a leading BOM is consumed. dotenv does NOT
    strip it, and parses the first key as "\\ufeffKEY" instead. Matching dotenv
    here would make this parser byte-identical on a BOM'd file, which is exactly
    why parser parity cannot be the safety property for a BOM -- a "don't strip
    the BOM" mutation scores as MORE dotenv-identical, not less. BOM safety comes
    from has_utf8_bom() below, which reports it and forces a non-zero exit no
    matter which parser is in use.
    """
    with open(path, encoding="utf-8-sig") as handle:
        lines = handle.read().splitlines()

    values = {}
    index = 0
    while index < len(lines):
        opened_at = index
        line = lines[index].strip()
        index += 1
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        if "=" not in line:
            values[line] = None
            continue

        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()

        quote = value[0] if value[:1] in ('"', "'") else ""
        if not quote:
            # Unquoted: a " #" starts a trailing comment.
            values[key] = value.split(" #", 1)[0].rstrip()
            continue

        body, end, index = _scan_for_close(lines, value[1:], quote, index)

        if end == -1:
            # Never closed, even at EOF. dotenv drops this binding and carries
            # on from the line after the one that opened the quote.
            if problems is not None:
                problems.append((opened_at + 1, key, "unterminated quote"))
            index = opened_at + 1
            continue

        trailing = body[end + 1:].strip()
        if trailing and not trailing.startswith("#"):
            # Closed, but with junk after the closing quote: dotenv discards the
            # binding and everything it swallowed getting there.
            if problems is not None:
                problems.append((opened_at + 1, key, "unterminated quote"))
            continue

        body = body[:end]
        values[key] = _decode_double_quoted(body) if quote == '"' else _decode_single_quoted(body)

    return values


try:
    from dotenv import dotenv_values
except ImportError:
    # python-dotenv lives in the lab's virtual environment. This check should still
    # work if you run it before "pip install -r requirements.txt", so fall back to
    # the equivalent stdlib reader defined above.
    dotenv_values = _parse_env_file


KNOWN_KEYS = ("AZURE_OPENAI_ENDPOINT", "MODEL_DEPLOYMENT")

# Which .env keys each task needs to run on its own.
TASK_REQUIREMENTS = {
    1: ["AZURE_OPENAI_ENDPOINT", "MODEL_DEPLOYMENT"],
    2: ["AZURE_OPENAI_ENDPOINT", "MODEL_DEPLOYMENT"],
    3: ["AZURE_OPENAI_ENDPOINT", "MODEL_DEPLOYMENT"],
    4: ["AZURE_OPENAI_ENDPOINT", "MODEL_DEPLOYMENT"],
}

# Tasks that also need the local grounding data.
TASKS_NEEDING_GUIDES = {4}

# Placeholder text shipped in .env.example - present but not yet filled in.
# The literals below are a fallback; find_placeholders() also reads the real
# .env.example at runtime, so editing that file can't silently leave this list
# stale and start reporting an untouched .env as ready.
PLACEHOLDERS = {
    "",
    "your_azure_openai_endpoint",
    "your_model_deployment",
    "<your_azure_openai_endpoint>",
    "<your_model_deployment>",
}

# How to fix each key, shown only when it's missing.
FIX_HINTS = {
    "AZURE_OPENAI_ENDPOINT": (
        "Copy the Azure OpenAI Endpoint (not the project endpoint) from your project "
        "home page in the Microsoft Foundry portal, then set AZURE_OPENAI_ENDPOINT in .env."
    ),
    "MODEL_DEPLOYMENT": (
        "Set MODEL_DEPLOYMENT to the exact name of your deployed model (for example, "
        "gpt-5.2). You can see it in the Foundry portal under Deployments."
    ),
}


def find_env_file():
    """Return the .env next to the lab's python folder, wherever this is run from."""
    here = Path(__file__).resolve().parent
    candidates = [
        Path.cwd() / ".env",
        here.parent / "python" / ".env",
        here.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # Default to the python-folder location even if it doesn't exist yet.
    return here.parent / "python" / ".env"


def find_guides_folder():
    """Return the guides folder used by Task 4, wherever this is run from."""
    here = Path(__file__).resolve().parent
    candidates = [
        Path.cwd() / "guides",
        here.parent / "python" / "guides",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return here.parent / "python" / "guides"


def find_quote_problems(env_path):
    """Line numbers of malformed quotes in the .env, whichever parser is in use.

    Always uses the local reader, because python-dotenv reports these to stderr
    rather than returning them, and the learner needs to be told which line to
    fix. dotenv silently drops the affected settings, so without this the
    preflight would just say a key is missing and never say why.
    """
    problems = []
    try:
        _parse_env_file(env_path, problems=problems)
    except OSError:
        return []
    return problems


def has_utf8_bom(env_path):
    """True if the .env starts with a UTF-8 BOM.

    Notepad (and other Windows editors) default to "UTF-8 with BOM". The BOM
    becomes part of the first key name, so load_dotenv() sets "\\ufeffKEY" and
    the app's os.getenv("KEY") returns None. It's a real defect that breaks the
    app, so it's reported rather than silently tolerated.
    """
    try:
        with open(env_path, "rb") as handle:
            return handle.read(3) == b"\xef\xbb\xbf"
    except OSError:
        return False


def _looks_like_url(value):
    """A project endpoint is always an https:// URL."""
    return value.startswith("https://") or value.startswith("http://")


def _looks_like_deployment_name(value):
    """A model deployment name is a bare name - never a URL, never spaced."""
    return not _looks_like_url(value) and not any(c.isspace() for c in value)


# Shape rules for settings whose form is known. These catch template text
# however it happens to be worded - a keyword list can always be out-worded,
# but an endpoint that isn't a URL is wrong no matter what it says. They also
# catch a learner pasting the right value into the wrong setting.
KEY_SHAPES = {
    "AZURE_OPENAI_ENDPOINT": (
        _looks_like_url,
        "This doesn't look like an endpoint - it must start with https://. Copy the "
        "Azure OpenAI endpoint (not the project endpoint) from your project home page "
        "in the Microsoft Foundry portal.",
    ),
    "MODEL_DEPLOYMENT": (
        _looks_like_deployment_name,
        "This doesn't look like a deployment name - it should be a bare name such as "
        "gpt-5.2, not a URL. Check you haven't pasted the endpoint here by mistake.",
    ),
}


def _looks_like_placeholder(value):
    """True only for text that is unmistakably fill-me-in.

    Deliberately conservative. A .env.example may legitimately ship a working
    default (a real model name, say), and treating that as a placeholder would
    block a learner who correctly kept it. So only obvious markers count.
    """
    lowered = value.strip().lower()
    if not lowered:
        return True
    if lowered.startswith("<") and lowered.endswith(">"):
        return True
    if "your" in lowered or "your-" in lowered:
        return True
    return lowered in {"changeme", "change-me", "change_me", "todo", "tbd",
                       "replace", "replaceme", "replace-me", "xxx", "..."}


def find_placeholders(env_path):
    """Placeholder values that mean "not filled in yet".

    Starts from the curated list above, then adds any obviously-placeholder
    text found in the shipped .env.example, so editing that file can't leave
    this check hunting for stale wording and calling an untouched .env ready.

    Values in .env.example that don't look like placeholders are left alone --
    a lab may ship a real working default, and that counts as set.
    """
    placeholders = set(PLACEHOLDERS)
    example = env_path.parent / ".env.example"
    if example.exists():
        try:
            for value in _parse_env_file(example).values():
                if value and _looks_like_placeholder(value):
                    placeholders.add(value)
        except OSError:
            pass
    return placeholders


def load_values(env_path):
    """Merge real environment variables over .env file values (env wins).

    A leading UTF-8 BOM is stripped from key names so the per-key report below
    stays readable; the BOM itself is reported separately by has_utf8_bom,
    because it still has to be fixed for the app to work.
    """
    values = {}
    if env_path.exists():
        try:
            parsed = dotenv_values(env_path)
        except OSError:
            # Unreadable (permissions, a directory, a half-written file): treat
            # it as empty and let the per-key report say what's missing.
            parsed = {}
        for key, value in parsed.items():
            if value is None:
                continue
            values[key.lstrip("\ufeff").removeprefix("export ").strip()] = value
    for key in KNOWN_KEYS:
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def is_set(values, key, placeholders=PLACEHOLDERS):
    """A key counts as set if it's present, not a placeholder, and the right shape."""
    value = (values.get(key) or "").strip().strip('"')
    if not value or value in placeholders:
        return False
    shape = KEY_SHAPES.get(key)
    return shape is None or shape[0](value)


def wrong_shape(values, key, placeholders=PLACEHOLDERS):
    """Message for a value that is present and not a placeholder, but malformed.

    Distinguishes "you haven't filled this in" from "you filled it in with the
    wrong thing", which are very different problems for a learner to debug.
    """
    value = (values.get(key) or "").strip().strip('"')
    if not value or value in placeholders:
        return None
    shape = KEY_SHAPES.get(key)
    if shape is None or shape[0](value):
        return None
    return f"{shape[1]} (found: {value!r})"


def main():
    parser = argparse.ArgumentParser(
        description="Check that your .env has what a given lab task needs."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=sorted(TASK_REQUIREMENTS),
        required=True,
        help="Which task you're about to start (1-4).",
    )
    args = parser.parse_args()

    env_path = find_env_file()
    values = load_values(env_path)
    placeholders = find_placeholders(env_path)
    required = TASK_REQUIREMENTS[args.task]

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

    missing = [key for key in required if not is_set(values, key, placeholders)]

    for key in required:
        mark = "OK " if is_set(values, key, placeholders) else "MISSING"
        print(f"  [{mark}] {key}")

    guides_problem = None
    if args.task in TASKS_NEEDING_GUIDES:
        guides = find_guides_folder()
        guide_files = sorted(guides.glob("*.md")) if guides.is_dir() else []
        if guide_files:
            print(f"  [OK ] guides/ ({len(guide_files)} destination guides)")
        else:
            print("  [MISSING] guides/")
            guides_problem = (
                "Task 4 uploads the Wingtip Journeys destination guides to a vector store. "
                f"Expected Markdown files in {guides}. Re-clone the mslearn-ai-studio repo "
                "if the folder is missing."
            )

    bom_problem = None
    if env_path.exists() and has_utf8_bom(env_path):
        print("  [PROBLEM] .env starts with a UTF-8 BOM")
        bom_problem = (
            "Your .env was saved as 'UTF-8 with BOM' (Notepad does this by default). "
            "The BOM becomes part of the first setting's name, so the app reads it as "
            "empty even though the file looks correct. Re-save the file as plain UTF-8: "
            "in VS Code, click the encoding in the status bar, choose 'Save with Encoding', "
            "then 'UTF-8' (not 'UTF-8 with BOM')."
        )

    quote_problem = None
    quote_warning = None
    quote_problems = find_quote_problems(env_path) if env_path.exists() else []
    if quote_problems:
        for line_number, key, _ in quote_problems:
            mark = "PROBLEM" if missing else "WARNING"
            print(f"  [{mark}] .env line {line_number}: unterminated quote ({key})")
        first_line, first_key, _ = quote_problems[0]
        explanation = (
            f"Line {first_line} opens a quote that is never closed. {first_key} is dropped, "
            "and if a later line contains a matching quote, every setting in between is "
            "swallowed into that value and dropped too. That's why a setting can look "
            "correct in the file and still read as empty. Close the quote (or remove both "
            "quotes) on that line."
        )
        if missing:
            # Something this task needs is absent, and bad quoting is the likely cause.
            quote_problem = explanation
        else:
            # Everything this task needs was still readable, so don't block on it --
            # the app will run. Say it anyway, because another setting is being lost.
            quote_warning = explanation

    if not missing and guides_problem is None and bom_problem is None and quote_problem is None:
        print()
        if quote_warning is not None:
            print("Warning: your .env has a quoting problem, but every setting this task")
            print("needs was still readable, so you can continue.")
            print(f"\n  .env quoting\n    {quote_warning}\n")
        print(f"You're ready to start Task {args.task}.")
        return 0

    print()
    print("Fix the following before starting this task:")
    for key in missing:
        detail = wrong_shape(values, key, placeholders) or FIX_HINTS.get(
            key, "Add this key to your .env file.")
        print(f"\n  {key}\n    {detail}")
    if guides_problem is not None:
        print(f"\n  guides/\n    {guides_problem}")
    if bom_problem is not None:
        print(f"\n  .env encoding\n    {bom_problem}")
    if quote_problem is not None:
        print(f"\n  .env quoting\n    {quote_problem}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
