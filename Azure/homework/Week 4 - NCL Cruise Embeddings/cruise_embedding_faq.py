from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain.chains import load_chain
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

def initialize_vectordb():
    # Initialize upon service startup...
    # Load the persisted database from disk, and use it as normal.
    persist_directory = 'faq_db' 
    embedding = OpenAIEmbeddings()

    return Chroma(persist_directory=persist_directory, embedding_function=embedding)

def initialize_question_answer(vectordb):
    prompt_template = """Use the following pieces of context to answer the question at the end. Limit your answer to only information about Norwegian Cruise Line. Never discuss competitors. Do not suggest the human visit a website as the answer. Provide as much of the relevant context in your answer as possible and provide alternative related options if available. If you don't know the answer, just politely say that you don't know; don't try to make up an answer.

    {context}

    Question: {question}
    """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=vectordb.as_retriever(search_kwargs={'k': 1}), chain_type_kwargs=chain_type_kwargs)
    return qa

def ask_a_question(qa, query):
    print("HUMAN: " + query)
    response = qa.run(query)
    print("\nASSISTANT: " + response + "\n\n")
    return response

vectordb = initialize_vectordb()
qa = initialize_question_answer(vectordb)

response = ask_a_question(qa, "My wife and I want to take a cruise, but are unsure if we should bring our kids. Are babysitters available?")

response = ask_a_question(qa, "In the context of NCL cruise, what does FCC mean?")

response = ask_a_question(qa, "How can I stay in touch with family and friends back home while I am on a cruise?")