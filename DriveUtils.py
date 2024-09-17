import os
import io
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive"]

#TODO Centralize service init
def DriveAuth():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


creds=DriveAuth()
def get_PDF_files() -> list:
    
    try:
        service = build("drive", "v3",credentials=creds)
        files = []
        page_token = None
        while True:
            response = (
                service.files()
                .list(
                    q="'1OmT4hJtwJ3B5wGBOyiM34EcWsfgDLf0U' in parents",
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                )
                .execute()
            )
            for file in response.get("files",[]):
                print(f'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get("files", []))
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
    except HttpError as error:
        print(f"An error occurred: {error}")
        files = None

    return files

def download_file(book) -> None:
    
    try:
    # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_id = book['id']

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")
        downloaded_file=open(f"../TheBooks/Pdf Books/{book['name']}",'xb')
        downloaded_file.write(file.getvalue())
        downloaded_file.close()

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return 


def get_books_to_be_added():
    books_in_drive=get_PDF_files()

    #Opening existing_books_file or creating one if it doesn't exist

    files_in_database=os.listdir()

    if "existing_books_file.txt" in files_in_database:

        existing_books_file=open("./existing_books_file.txt",'r')
        existing_books=existing_books_file.readlines()
        existing_books_file.close()

    else:

        existing_books_file=open("./existing_books_file.txt",'x')
        existing_books=["no existing books yet"]
        existing_books_file.close()

    #Checking what books exist in the database 

    books_to_be_added=[]

    for book in books_in_drive:

        if f'{book['name']}\n' in existing_books:
            print(f"{book['name']} allready added!")
        else:
            books_to_be_added.append(book)

    return books_to_be_added