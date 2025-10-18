def get_files_info(working_directory, directory="."):
    '''
    always return a string for the LLM to handle errors gracefully
    '''
    import os

    target_directory = os.path.join(working_directory, directory)

    # Validate target directory is within the working directory boundaries
    if os.path.abspath(working_directory) not in os.path.abspath(target_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Validate target directory is a directory
    if not os.path.isdir(target_directory):
        return f'Error: "{target_directory}" is not a directory'

    # list contents
    contents = os.listdir(target_directory)

    # initialize response string
    response = ""

    # construct response from each item
    for item in contents:
        try:
            item_path = os.path.join(target_directory, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            response += f'- {item}: file_size={file_size} bytes, is_dir={is_dir}\n'
        except Exception as e:
            return f"Error: {str(e)}"
        
    return response.strip()