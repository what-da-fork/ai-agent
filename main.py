import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# system prompt
system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

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
    config=types.GenerateContentConfig(system_instruction=system_prompt)
)

def main():
    if verbose:
        print(f"User prompt: {prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print(response.text)

if __name__ == "__main__":
    main()
