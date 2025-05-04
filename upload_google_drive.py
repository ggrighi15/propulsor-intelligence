
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# Caminho para o arquivo da conta de serviço
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Nome do arquivo gerado
FILE_NAME = 'output_card.png'
MIME_TYPE = 'image/png'

# ID da pasta no Google Drive compartilhada com a conta de serviço (se tiver)
FOLDER_ID = None  # ou substitua com ID da pasta

def upload_file():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': FILE_NAME}
    if FOLDER_ID:
        file_metadata['parents'] = [FOLDER_ID]

    media = MediaFileUpload(FILE_NAME, mimetype=MIME_TYPE)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"✅ Arquivo enviado com ID: {file.get('id')}")

if __name__ == '__main__':
    upload_file()
