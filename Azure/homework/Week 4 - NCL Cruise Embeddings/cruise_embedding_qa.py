from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
#from langchain import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain.chains import load_chain
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.llms import Bedrock

import os

class CruiseEmbeddingQA:
    def __init__(self, vector_db_path, silent=True, llm=None, embedding=None):
        self._silent = silent
        if llm is None:
            model_name = 'gpt-3.5-turbo'
            temperature = 0.5
            self._llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        else:
            self._llm = llm
        if embedding is None:
            self._embedding = OpenAIEmbeddings()
        else:
            self._embedding = embedding

        # Initialize vector db for embeddings
        embedding = self._embedding
        self._vectordb = Chroma(persist_directory=vector_db_path, embedding_function=embedding)

        # Initialize the question-answer chain
        self._qa = self.initialize_question_answer()

    def initialize_question_answer(self):
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        Limit your answer to only information about Norwegian Cruise Line. Never discuss competitors. 
        Do not suggest the human visit a website as the answer. 
        Provide some explanation of your reasoning when making recommendations. 
        If you don't know the answer, just say that you don't know; don't try to make up an answer.

        {context}

        Question: {question}
        """

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}
        qa = RetrievalQA.from_chain_type(llm=self._llm, chain_type="stuff", retriever=self._vectordb.as_retriever(), chain_type_kwargs=chain_type_kwargs)
        return qa

    def ask_a_question(self, query):
        if not self._silent:
            print("HUMAN: " + query);
        response = self._qa.run(query)
        if not self._silent:
            print("\nASSISTANT: " + response + "\n")
        return response

    @staticmethod
    def getBedrockLlm(model_id='st.session_state["llm_model"]'):
        llm = Bedrock(
            credentials_profile_name="default",
            region_name="us-east-1",
            model_id = model_id,
        )

        return llm

    @staticmethod
    def getBedrockEmbedding():
        be = BedrockEmbeddings(
            credentials_profile_name="default",
            region_name="us-east-1",
            model_id = "amazon.titan-e1t-medium",
        )
        return be

if __name__ == "__main__":
    USE_BEDROCK = os.getenv('USE_BEDROCK') or "false"
    if USE_BEDROCK.lower() == "true":
        print('\n\nUSING BEDROCK\n\n')
        db_path = "bedrock_db"
        llm = CruiseEmbeddingQA.getBedrockLlm()
        embedding = CruiseEmbeddingQA.getBedrockEmbedding()
        cruise_qa = CruiseEmbeddingQA(db_path, False, llm, embedding)
    else:    
        db_path = "db"
        cruise_qa = CruiseEmbeddingQA(db_path, False)

    response = cruise_qa.ask_a_question("My wife and I want to take a cruise and go snorkeling. We live in Sarasota, FL. We do not want to have to fly to the departure port. Please recommend cruises. In your response, explain why this is a great cruise option for me.")
    response = cruise_qa.ask_a_question("My wife and I want to take a cruise and go snorkeling. We live in Sarasota, FL. We do not want to have to fly to the departure port.")
    response = cruise_qa.ask_a_question("Which type of cruise stateroom should I consider on the Norwegian Sky. Please help me decide by discussing options and why one might choose each.")
    response = cruise_qa.ask_a_question("My wife and I are history buffs. Where should we go?")
    response = cruise_qa.ask_a_question("My wife and I want to see penguins. Where should we go?")