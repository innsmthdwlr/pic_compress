import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient import errors


class PictureRepository:

    def __init__(self, credentials):
        self.service = build('drive', 'v3', credentials=credentials)

    def get_file_list(self, directory_name):
        page_token = None
        drive_filenames = {}
        while True:
            response = self.service.files().list(
                q=f"name = '{directory_name}'").execute()
            directory_id = ""
            for f in response.get('files', []):
                directory_id = f.get('id')

            response = self.service.files().list(
                q=f"'{directory_id}' in parents").execute()
            for f in response.get('files', []):
                drive_filenames[f.get('name')] = f.get('id')

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return drive_filenames

    def download_file(self, file_id, file_name, directory_path):
        file_path = os.path.join(directory_path, file_name)

        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print(f"Download {int(status.progress() * 100)}")

        with io.open(file_path, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())

    def delete_file(self, file_id):
        try:
            self.service.files().delete(fileId=file_id).execute()
        except errors.HttpError:
            print('An error occured, could not delete the file')
