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

# Function map
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

# system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

First, analyze the user's request and determine which functions to call. You may need to call multiple functions in sequence to fulfill the user's request. After each function call, you will receive the result which you can use to inform your next steps.
Determine your working directory by calling get_files_info with directory ".".

Be thorough in your analysis and response.

When analyzing code, ensure you break down how it works and what each part does.

Never incldue code files or their contents directly in your responses unless explicitly asked by the user.
"""

# CLI args
verbose = "--verbose" in sys.argv
if verbose:
    sys.argv.remove("--verbose")

if len(sys.argv) <= 1:
    print("please provide a prompt")
    sys.exit(1)

prompt = sys.argv[1]

# function to call functions
def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    try:
        called_function = FUNCTION_MAP[function_call_part.name]
    except KeyError:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    try:
        result = called_function(
            working_directory=os.path.abspath(BASE_PATH),
            **function_call_part.args,
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": str(e)},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

def main():
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    max_iterations = 20
    i = 0

    while i < max_iterations:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            print(f"Error during content generation: {e}")
            sys.exit(1)

        # keep chat context
        messages.append(response.candidates[0].content)

        if verbose:
            print(f"User prompt: {prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # handle function calls
        if response.function_calls:
            for call in response.function_calls:
                print(f"Function call representation: {repr(call)}")
                function_result = call_function(call, verbose=verbose)
                messages.append(function_result)

                if not function_result.parts[0].function_response.response:
                    raise Exception("Fatal - No function response received.")
                if function_result.parts[0].function_response.response and verbose:
                    print(f"-> {function_result.parts[0].function_response.response}")

            # continue to next iteration so Gemini sees tool outputs
            i += 1
            continue  

        # no more function calls — final response
        if response.text:
            print(response.text)
            break # exit loop if we have a text response

        if not response.function_calls:
            print(response.text)

        # always increment iteration counter
        i += 1
        
    else:
        print(f"Reached maximum iteration limit ({max_iterations}) without final text response.")

# Main execution
if __name__ == "__main__":
    main()
