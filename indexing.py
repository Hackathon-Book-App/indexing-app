#Getting book titles to be added

from DriveUtils import get_books_to_be_added

books_to_be_added=get_books_to_be_added()

#Loading API Key

from dotenv import load_dotenv
load_dotenv(".venv/.env")

#Initiating vectorstore from client (the one on RPi)

import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

client=chromadb.HttpClient(host="https://better-skink-promoted.ngrok-free.app",port=8000)

vectorstore = Chroma(client=client, embedding_function=OpenAIEmbeddings(show_progress_bar=True))

#Adding new books to the database   

from langchain_community.document_loaders import PyPDFLoader
from DriveUtils import download_file

#Initiating text splitter

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

for book in books_to_be_added:

    #Loadig book PDF

    print(f"... Loading '{book['name']}' ... \n")
    
    download_file(book)

    book_path = f'../TheBooks/Pdf Books/{book['name']}' #TODO implement downloading and loading from drive
    loader = PyPDFLoader(book_path)

    docs = loader.load()

    print(f"... Loaded '{book}' ...\n")

    #Spliting, embedding and adding to the vectorstore

    splits = text_splitter.split_documents(docs)
    
    vectorstore.add_documents(splits)
    
    #Adding book to existing books record

    existing_books_file=open("./existing_books_file.txt",'a')
    existing_books_file.write(book["name"]+'\n')
    existing_books_file.close()
    
    print(f'\n... Finished "{book}" ...\n')
    
