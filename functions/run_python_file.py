import subprocess
import os
from google.genai import types

# need to see how to best handle args from LLM as an optional input
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Gets the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to execute, relative to the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):

    target_file = os.path.join(working_directory, file_path)
    abs_target_file = os.path.abspath(target_file)

    # Validate target file_path is within the working directory boundaries
    if os.path.abspath(working_directory) not in os.path.abspath(target_file):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Validate target file_path exists
    if not os.path.exists(abs_target_file):
        return f'Error: File "{file_path}" not found.'
    
    # Validate file_path is a .py file
    if not abs_target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python", abs_target_file] + args,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
            cwd=working_directory
        )
        return f"STDOUT:{result.stdout}\nSTDERR:{result.stderr}\n{f'Process exited with code {result.returncode}' if result.returncode != 0 else 'No output produced.'}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
