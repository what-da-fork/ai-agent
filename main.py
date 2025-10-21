import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import BASE_PATH
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Declare available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Initialize verbose flag
verbose = False

# Parse arguments
if "--verbose" in sys.argv:
    verbose = True
    sys.argv.remove("--verbose")

if len(sys.argv) <= 1:
    print("please provide a prompt")
    sys.exit(1)

prompt = sys.argv[1]  

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
                                       )
)

def main():
    if verbose:
        print(f"User prompt: {prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Function call representation: {repr(function_call_part)}")
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            if function_call_part.name == "get_files_info":
                raw_dir = function_call_part.args.get("directory")
                directory = raw_dir.strip() if isinstance(raw_dir, str) and raw_dir.strip() else "."
                function_response = get_files_info(
                    working_directory=os.path.abspath(BASE_PATH),
                    directory=directory
                )
                print(f"Function response:\n{function_response}\n")
    if not response.function_calls:
        print(response.text)

if __name__ == "__main__":
    main()
