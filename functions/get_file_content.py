
from config import MAX_CHARS

'''
Now that we have a function that can get the contents of a directory, we need one that can get the contents of a file. 
Again, we'll just return the file contents as a string, or perhaps an error string if something went wrong.

As always, we'll safely scope the function to a specific working directory.
'''

def get_file_content(working_directory, file_path):
    import os

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