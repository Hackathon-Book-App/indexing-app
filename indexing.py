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

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(), persist_directory="..\\embeddedBooksDB")
