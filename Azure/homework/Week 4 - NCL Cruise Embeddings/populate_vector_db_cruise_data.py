#Populate the vector database
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.chains import load_chain
from langchain_community.embeddings import BedrockEmbeddings

# Load the text file containing the data to be embedded via vector database
loader_data = TextLoader("./scrape_cruise_data/cruise_data.txt")
documents = loader_data.load()

# Split the document into chunks
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk

# Bedrock
#try:
#    persist_directory = "bedrock_db"
#    region_name ="us-east-1"
#    model_id = "`amazon.titan-e1t-medium`"
#
#    embedding = BedrockEmbeddings(
#        credentials_profile_name="default",
#        region_name="us-east-1",
#        model_id = "amazon.titan-e1t-medium"
#    )
#    vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)
#    vectordb.persist()
#    vectordb = None
#except:
#    print("Error populating the Bedrock embeddings database")
#finally: 
#    vectordb = None


# OpenAI
#try: 
persist_directory = 'db'
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)
vectordb.persist()
#except:
#    print("Error populating the OpenAI embeddings database")
#finally:
#    vectordb = None