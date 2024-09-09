#Loading API Key
from dotenv import load_dotenv

load_dotenv(".venv/.env")

#Initiating vectorestore

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma(embedding_function=OpenAIEmbeddings(show_progress_bar=True), persist_directory="..\\embeddedBooksDB")

#Initiating text splitter

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

#Getting book titles to be added

import os
books_in_folder=os.listdir("../TheBooks/Pdf Books")

#Opening existing_books_file or creating one if it doesn't exist

files_in_database=os.listdir("../embeddedBooksDB")

if "existing_books_file.txt" in files_in_database:
        
    existing_books_file=open("../embeddedBooksDB/existing_books_file.txt",'r')
    existing_books=existing_books_file.readlines()
    existing_books_file.close()

else:

    existing_books_file=open("../embeddedBooksDB/existing_books_file.txt",'x')
    existing_books=["no existing books yet"]
    existing_books_file.close()

print("These are the existing books")
for book in existing_books: 
    print(book)
print('\n\n')

#Checking what books exist in the database 

books_to_be_added=[]

for book in books_in_folder:
    
    if f'{book}\n' in existing_books:
        print(f"{book} allready added!")
    else:
        books_to_be_added.append(book)

#Adding new books to the database   

from langchain_community.document_loaders import PyPDFLoader

for book in books_to_be_added:

    #Adding book to existing books record

    existing_books_file=open("../embeddedBooksDB/existing_books_file.txt",'a')
    existing_books_file.write(book+'\n')
    existing_books_file.close()

    #Loadig book PDF

    print(f"... Loading '{book}' ... \n")
    
    book_path = f'../TheBooks/Pdf Books/{book}'
    loader = PyPDFLoader(book_path)

    docs = loader.load()

    print(f"... Loaded '{book}' ...\n")

    #Spliting, embedding and adding to the vectorstore

    splits = text_splitter.split_documents(docs)
    
    vectorstore.add_documents(splits)
    
    print(f'\n... Finished "{book}" ...\n')
    
