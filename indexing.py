#TODO epub, mobi, audiobook, grafic novels support

from Utils import get_books_to_be_added

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

from Utils import LoadBookAndSplit

for book in books_to_be_added:
    
    splits=LoadBookAndSplit(book)
    
    vectorstore.add_documents(splits)

    #Adding book to existing books record

    existing_books_file=open("./existing_books_file.txt",'a')
    existing_books_file.write(book["name"]+'\n')
    existing_books_file.close()

    print(f'\n... Finished "{book}" ...\n')