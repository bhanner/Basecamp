# README

> Cruise data example code using OpenAI, LangChain, and Chroma vectordb embeddings to perform question/answer based on a sampling of NCL cruise data (all data publicly available, sourced from their public internet website)

## How to use this sample code

### Setup

* Have current versions of python3 and pip installed
* Run `pip install -r requirements.txt` to install dependencies
* Set an environment variable with an OpenAI API token.
  * On a Mac:
    `echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc && source ~/.zshrc`
  * For other setups, see this article for guidance: https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety

## Optional: Scrape data from public URLs

* The directory `scrape_cruise_data` contains a python script (and list of URLs to scrape) which will populate the `cruise_data.txt` file. A pre-populated `cruise_data.txt` file is provided in the repo, so running the scraper is optional.

## Populating the vector db for cruise data

* Run `python3 populate_vector_db_cruise_data.py`. This will load the `cruise_data.txt` file, chunk the file, and calculate embeddings vectors for each chunk. It will create a directory named `db`, and populate a Chroma vector database with the embedding vectors.

## Populating the vector db for frequently asked questions

* Run `python3 populate_vector_db_faq.py`. This will load the `cruise-faq.json` file, chunk the file, and calculate embeddings vectors for each chunk. It will create a directory named `faq_db`, and populate a Chroma vector database with the embedding vectors.

## Running the question/answer sample queries for cruise data

* Run `python3 cruise_embedding_qa.py`.  The responses to the queries in the sample script will be displayed in the terminal.

## Running the question/answer sample queries for faq data

* Run `python3 cruise_embedding_faq.py`.  The responses to the queries in the sample script will be displayed in the terminal.

## Opening the UI

* Run `streamlit run ui.py`.  This should open up Streamlit UI. This UI will let you to provide OpenAI Key via a textbox in left pane 


## Using Bedrock
### Pre-Requisites

Before you may continue, you will need to satisfy some pre-requisites outlined below.

1. You need access to a Slalom AWS Innovation Lab having AWS Bedrock. As of 8/25/23, that means you need access to the Beta1 Slalom AWS Innovation Lab. If you do not have access, [you can request it on this page](https://slalom.service-now.com/support?id=sc_cat_item&sys_id=d429ad4a1bea4d904c03419ead4bcb50&sysparm_category=271e14a987e2891004b4ba6f8bbb3502). Be sure to choose the Beta1 Innovation Lab (or another environment with Bedrock, though as of 8/25/23, the Beta1 was the only one)
2. You have set up your aws profile on your machine, and it is set to assume a Beta1 innovation lab role. You would use the `aws configure` command tool to manage your profiles. [This article](https://medium.com/nerd-for-tech/configuration-and-credential-file-settings-in-aws-cli-61c7ff0a1cd6) also provides some guidance. Check the Role ARN to be sure the role you are assuming is associated with the correct account (Beta1 account as of 8/25/23). 
3. You can use the terminal (command-line) tool [aws-azure-login](https://slalom.atlassian.net/wiki/spaces/INFRA/pages/2923855887/AWS+CLI+Setup+Troubleshooting+aws-azure-login) to use Single Sign On to generate AWS Access Key and Secret Key.
4. You have python3 installed and configured on your machine
5. You have the ability to run Jupyter Notebooks on your machine.

### Creating a Python Virtual Environment
Assuming you are starting from this directory, and it is called `cruise_openai_embeddings_example`
```
cd ../
python -m venv cruise_openai_embeddings_example && \
source ./cruise_openai_embeddings_example/bin/activate
```

### Download Updated Boto3 and Botocore Python Modules

[Use this link to download a compressed file](https://d2eo22ngex1n9g.cloudfront.net/Documentation/SDK/bedrock-python-sdk.zip) containing the needed modules. As of 8/25/23, you need to use "special" versions of these modules, since Bedrock is in preview. The general modules do not have support. Unzip the file. Install the modules.
```
mkdir -p ./downloaded_modules/extracted && \
curl https://d2eo22ngex1n9g.cloudfront.net/Documentation/SDK/bedrock-python-sdk.zip -o downloaded_modules/bedrock-python-sdk.zip && \
unzip -o downloaded_modules/bedrock-python-sdk -d downloaded_modules/extracted && \
cd ./cruise_openai_embeddings_example/ && \
python -m pip install ../downloaded_modules/extracted/botocore-1.31.21-py3-none-any.whl && \
python -m pip install ../downloaded_modules/extracted/boto3-1.28.21-py3-none-any.whl && \
cd ..
```

### Install other dependencies
```
python -m pip install -r requirements.txt
```
### Reminder - Be sure you logged in to aws and your tokens are still valid

Open a terminal and enter 
```
aws-azure-login
```