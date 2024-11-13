from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI()

load_dotenv()

user_question = "Are babysitters available?"

test_messages = []
test_messages.append({"role": "system", "content": "You are an assistant providing information about Norwegian Cruise Line services."})
test_messages.append({"role": "user", "content": user_question})

response =  client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:personal:ne-se-gen-ai-boot-camp-2024-11-05:AQLJXOuL",
    messages=test_messages,
    temperature=0.8,
    max_tokens=200,
    stream=False
)
print(user_question)
print(response.choices[0].message.content)
