import os
import sys
from openai import OpenAI

def main():
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    while True:
        # Get user input
        prompt = input("Enter your prompt: ")

        if prompt == 'done':
            break
        
        # Make API call
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Print response
            print(completion.choices[0].message.content)

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()