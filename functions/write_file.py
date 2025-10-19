def write_file(working_directory, file_path, content):
    import os

    target_file = os.path.join(working_directory, file_path)
    abs_target_file = os.path.abspath(target_file)

    # Validate target file_path is within the working directory boundaries
    if os.path.abspath(working_directory) not in os.path.abspath(target_file):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(abs_target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"