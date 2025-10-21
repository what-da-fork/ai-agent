
import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    target_file = os.path.join(working_directory, file_path)
    abs_target_file = os.path.abspath(target_file)

    # Validate target file_path is within the working directory boundaries
    if os.path.abspath(working_directory) not in os.path.abspath(target_file):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Validate target file_path is a file
    if not os.path.isfile(abs_target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {str(e)}"
    
    return file_content_string