from langchain_community.document_loaders import PyPDFDirectoryLoader

directory_path = "C:\\Users\\raoul\\source\\Myprojects\\Hackathon\\TheBooks\\Pdf Books"
loader = PyPDFDirectoryLoader(directory_path)

docs = loader.load()

print(len(docs))

from dotenv import load_dotenv
load_dotenv(".venv/.env")


from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma(collection_name="booksEmbeddings",embedding_function=OpenAIEmbeddings(), persist_directory="..\\embeddedBooksDB")

from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils.batch_utils import create_batches

# import chromadb.utils.embedding_functions as embedding_functions
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key="OPENAI_API_KEY",
#                 model_name="text-embedding-ada-002"
#             )


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

for batch in create_batches(
    api=vectorstore._client,
    ids=[doc.id for doc in splits],
    metadatas=[doc.metadata for doc in splits],
    documents=[doc.page_content for doc in splits],
):
    
    vectorstore._chroma_collection.add(*batch)