# AI Agent

Lightweight AI coding agent that uses the Gemini API to inspect and manipulate a project workspace. The agent exposes a small set of safe tooling functions (list files, read files, run Python, write files) and drives multi-step function-call plans from user prompts.

## Features
- List files and directories within a confined working directory
- Read file contents
- Execute Python files (with argument passing) under working directory constraints
- Write or overwrite files (restricted to project scope)
- CLI interface with optional `--verbose` flag for diagnostic output

## Quick start

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies (project uses Poetry/pyproject; fallback shown):
```bash
pip install -r requirements.txt || pip install -e .
```

3. Create a `.env` file with your Gemini API key:
```text
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the agent:
```bash
python main.py "Please list files in the project"
# with verbose output:
python main.py --verbose "Please list files in the project"
```

## CLI
- Positional argument: the user prompt (required)
- Optional flag: `--verbose` — prints token counts, function call details, and tool outputs to console

Example parsing in code:
- `verbose = "--verbose" in sys.argv` (then `sys.argv.remove("--verbose")` so prompt remains at `sys.argv[1]`)

## Functions exposed to the model
- get_files_info(directory=".") -> string: lists directory contents and sizes
- get_file_content(file_path) -> string: returns file contents or error
- run_python_file(file_path, args=[]) -> string: runs a .py file and returns stdout/stderr (timeout and sandboxing enforced)
- write_file(file_path, content) -> string: write or overwrite file, restricted to allowed paths

All functions accept a `working_directory` injected by the runner; paths must be relative and stay inside the working directory.

## Project layout
- main.py — entry point and orchestration of prompt → model → function calls → responses
- functions/ — implementations of the tools listed above
- calculator/ — sample project used for testing
- tests.py — ad-hoc tests (not pytest-style by default)

## Testing
- Quick: run the tests script directly to execute helper functions:
```bash
python tests.py
```
- For pytest-style tests, rename files to `test_*.py` and use:
```bash
pytest -s
```

## Troubleshooting
- "Missing API key": ensure `.env` is present and `GEMINI_API_KEY` is set or exported.
- "UnboundLocalError: messages": avoid using `messages += ...` inside functions; use `messages.append(...)`/`extend(...)` to mutate the list.
- "non-text parts in the response": the SDK can return structured FunctionResponse objects. Extract the textual `result` before appending to `messages` (append a `types.Part(text=...)`) so the model receives plain text tool outputs.
- Access function calls from response via `response.function_calls` (not `function_call_part`).

## Security notes
- Paths are validated to prevent escaping the working directory.
- Executing arbitrary Python code is constrained (timeout, working directory checks). Treat this project as experimental; do not run with untrusted prompts on sensitive systems.

## Contributing
Open issues or PRs for fixes, improved safety checks, or new tooling functions.

```// filepath: /home/m/workspace/github.com/what-da-fork/ai-agent/README.md
# AI Agent

Lightweight AI coding agent that uses the Google Generative AI (Gemini) API to inspect and manipulate a project workspace. The agent exposes a small set of safe tooling functions (list files, read files, run Python, write files) and drives multi-step function-call plans from user prompts.

## Features
- List files and directories within a confined working directory
- Read file contents
- Execute Python files (with argument passing) under working directory constraints
- Write or overwrite files (restricted to project scope)
- CLI interface with optional `--verbose` flag for diagnostic output

## Quick start

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies (project uses Poetry/pyproject; fallback shown):
```bash
pip install -r requirements.txt || pip install -e .
# or: poetry install
```

3. Create a `.env` file with your Gemini API key:
```text
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the agent:
```bash
python main.py "Please list files in the project"
# with verbose output:
python main.py --verbose "Please list files in the project"
```

## CLI
- Positional argument: the user prompt (required)
- Optional flag: `--verbose` — prints token counts, function call details, and tool outputs to console

Example parsing in code:
- `verbose = "--verbose" in sys.argv` (then `sys.argv.remove("--verbose")` so prompt remains at `sys.argv[1]`)

## Functions exposed to the model
- get_files_info(directory=".") -> string: lists directory contents and sizes
- get_file_content(file_path) -> string: returns file contents or error
- run_python_file(file_path, args=[]) -> string: runs a .py file and returns stdout/stderr (timeout and sandboxing enforced)
- write_file(file_path, content) -> string: write or overwrite file, restricted to allowed paths

All functions accept a `working_directory` injected by the runner; paths must be relative and stay inside the working directory.

## Project layout
- main.py — entry point and orchestration of prompt → model → function calls → responses
- functions/ — implementations of the tools listed above
- calculator/ — sample project used for testing
- tests.py — ad-hoc tests (not pytest-style by default)

## Testing
- Quick: run the tests script directly to execute helper functions:
```bash
python tests.py
```
- For pytest-style tests, rename files to `test_*.py` and use:
```bash
pytest -s
```

## Troubleshooting
- "Missing API key": ensure `.env` is present and `GEMINI_API_KEY` is set or exported.
- "UnboundLocalError: messages": avoid using `messages += ...` inside functions; use `messages.append(...)`/`extend(...)` to mutate the list.
- "non-text parts in the response": the SDK can return structured FunctionResponse objects. Extract the textual `result` before appending to `messages` (append a `types.Part(text=...)`) so the model receives plain text tool outputs.
- Access function calls from response via `response.function_calls` (not `function_call_part`).

## Security notes
- Paths are validated to prevent escaping the working directory.
- Executing arbitrary Python code is constrained (timeout, working directory checks). Treat this project as experimental; do not run with untrusted prompts on sensitive systems.