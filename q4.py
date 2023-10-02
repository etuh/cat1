from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Define the path to your JSON credentials file
credentials_file = 'path/to/your/credentials.json'

# Initialize the Google Drive API client
credentials = service_account.Credentials.from_service_account_file(
    credentials_file, scopes=['https://www.googleapis.com/auth/drive']
)
drive_service = build('drive', 'v3', credentials=credentials)

# Define the folder ID where you want to upload files
folder_id = 'your_folder_id'

# List the files in the folder and upload them
folder_contents = os.listdir('path/to/your/files')
for file_name in folder_contents:
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(
        os.path.join('path/to/your/files', file_name),
        resumable=True
    )
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print(f'Uploaded: {file_name} (File ID: {file["id"]})')
