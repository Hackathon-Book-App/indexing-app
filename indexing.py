from langchain_community.document_loaders import PyPDFDirectoryLoader

directory_path = "C:\\Users\\raoul\\source\\Myprojects\\Hackathon\\TheBooks\\Pdf Books"
loader = PyPDFDirectoryLoader(directory_path)

docs = loader.load()

print(len(docs))

from dotenv import load_dotenv
load_dotenv(".venv/.env")


from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils.batch_utils import create_batches
import uuid
import chromadb

client = chromadb.PersistentClient(path="../EmbeddedBooks",settings=chromadb.Settings(allow_reset=True))
client.reset()

# import chromadb.utils.embedding_functions as embedding_functions
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key="OPENAI_API_KEY",
#                 model_name="text-embedding-ada-002"
#             )

colection=client.get_or_create_collection("bookEmbeddings",embedding_function=OpenAIEmbeddings)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)


for batch in create_batches(
    api=client,
    ids=[str(uuid.uuid4()) for _ in range(len(splits))],
    metadatas=[doc.metadata for doc in splits],
    documents=[doc.page_content for doc in splits],
):
    
    colection.add(ids=batch[0],
                   documents=batch[3],
                   embeddings=batch[1],
                   metadatas=batch[2])

    vectortore= Chroma(client=client, collection_name=colection.name, embedding_function=OpenAIEmbeddings)

