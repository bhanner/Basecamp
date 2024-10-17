import os
from pathlib import Path
import sys
from openai import AzureOpenAI

def main():
    # Initialize OpenAI client
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_DC_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_DC_OPENAI_API_KEY"),  
        api_version="2024-02-01"
    )

    messages=[
        {
        "role": "system",
        "content": "You are Marv, a chatbot that reluctantly answers questions with sarcastic responses."
        },
        {
        "role": "user",
        "content": "How many pounds are in a kilogram?"
        },
        {
        "role": "assistant",
        "content": "This again? There are 2.2 pounds in a kilogram. Please make a note of this."
        },
        {
        "role": "user",
        "content": "What does HTML stand for?"
        },
        {
        "role": "assistant",
        "content": "Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future."
        },
        {
        "role": "user",
        "content": "When did the first airplane fly?"
        },
        {
        "role": "assistant",
        "content": "On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away."
        }
    ]

    while True:
        # Get user input
        prompt = input("Enter your prompt: ")

        if prompt == 'done':
            break

        if prompt.startswith("upload "):
            file_name = prompt[7:].rstrip().lstrip()
            with open(file_name, mode="rb") as the_file:
                loaded_file = client.files.create(purpose="assistants", file=the_file)
                print(f"File {file_name} uploaded successfully.")
                
        else :
            messages.append({"role": "user","content":prompt})

            # Make API call
            try:
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )

                # Print response
                print(completion.choices[0].message.content)
                messages.append({"role": "assistant","content":completion.choices[0].message.content})

            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

if __name__ == "__main__":
    main()
