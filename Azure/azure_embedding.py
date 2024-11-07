import os
import re
import requests
import sys
from num2words import num2words
import os
import pandas as pd
import numpy as np
import tiktoken
from openai import AzureOpenAI

df=pd.read_csv(os.path.join(os.getcwd(),'bill_sum_data.csv')) # This assumes that you have placed the bill_sum_data.csv in the same directory you are running Jupyter Notebooks
print("--------------------------------------------------------------------------------------------------")
print(df)
print("--------------------------------------------------------------------------------------------------")

df_bills = df[['text', 'summary', 'title']]
print("--------------------------------------------------------------------------------------------------")
print(df_bills)
print("--------------------------------------------------------------------------------------------------")

pd.options.mode.chained_assignment = None #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#evaluation-order-matters

# s is input text
def normalize_text(s, sep_token = " \n "):
    s = re.sub(r'\s+',  ' ', s).strip()
    s = re.sub(r". ,","",s)
    # remove all instances of multiple spaces
    s = s.replace("..",".")
    s = s.replace(". .",".")
    s = s.replace("\n", "")
    s = s.strip()
    
    return s

df_bills['text']= df_bills["text"].apply(lambda x : normalize_text(x))

tokenizer = tiktoken.get_encoding("cl100k_base")
df_bills['n_tokens'] = df_bills["text"].apply(lambda x: len(tokenizer.encode(x)))
df_bills = df_bills[df_bills.n_tokens<8192]
len(df_bills)

print("--------------------------------------------------------------------------------------------------")
print(df_bills)
print("--------------------------------------------------------------------------------------------------")
sample_encode = tokenizer.encode(df_bills.text[0]) 
decode = tokenizer.decode_tokens_bytes(sample_encode)

print("--------------------------------------------------------------------------------------------------")
print(decode)
print("--------------------------------------------------------------------------------------------------")

len(decode)

client = AzureOpenAI(
    azure_endpoint = os.getenv("AZURE_BOSTON_OPENAI_ENDPOINT"), 
    api_key=os.getenv("AZURE_BOSTON_OPENAI_API_KEY"),  
    api_version="2024-02-01"
)

def generate_embeddings(text, model="text-embedding-3-small"): # model = "deployment_name"
    return client.embeddings.create(input = [text], model=model).data[0].embedding

df_bills['ada_v2'] = df_bills["text"].apply(lambda x : generate_embeddings (x, model = 'text-embedding-3-small')) # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model

print("--------------------------------------------------------------------------------------------------")
print(df_bills)
print("--------------------------------------------------------------------------------------------------")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_embedding(text, model="text-embedding-3-small"): # model = "deployment_name"
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def search_docs(df, user_query, top_n=4, to_print=True):
    embedding = get_embedding(
        user_query,
        model="text-embedding-3-small" # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    )
    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )
    return res

def main():
    res = None
    while True:
        # Get user input
        prompt = input("Enter your prompt or summary request: ")

        if prompt == 'done':
            break

        if prompt.startswith('summary of number:'):
            print(prompt[18:].rstrip().lstrip())
            # convert string to number
            num = int(prompt[18:].rstrip().lstrip())
            print(res["summary"][num])
        else:
            try:
                res = search_docs(df_bills, prompt, top_n=4)
                print(res)

            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

if __name__ == "__main__":
    main()

# res = search_docs(df_bills, "Can I get information on cable company tax revenue?", top_n=4)
# print("--------------------------------------------------------------------------------------------------")
# print(res)
# print("--------------------------------------------------------------------------------------------------")

# res["summary"][9]
# print("--------------------------------------------------------------------------------------------------")
# print(res["summary"][9])
# print("--------------------------------------------------------------------------------------------------")

