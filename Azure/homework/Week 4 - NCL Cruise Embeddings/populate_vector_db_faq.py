#Populate the vector database
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain_community.document_loaders import TextLoader
from langchain.chains import load_chain

# This repo is missing the cruise-faq.json file, so this won't run.

# Load the text file containing the data to be embedded via vector database
loader_faq = TextLoader("./cruise-faq.json")
documents = loader_faq.load()

# Split the document into chunks
text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
persist_directory = 'faq_db'

embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)

# Persist the database
vectordb.persist()
vectordb = None