import os.path
from src.auth import Auth
from src.picture_repository import PictureRepository
from src.picture_transform import PictureTransformator
# from picture_transform import PictureTransformator


def get_pictures_from_google(cwd, SCOPES, google_drive_dir, save_local_dir):
    # get files
    auth = Auth(cwd, SCOPES)
    google_drive = PictureRepository(auth.get_credentials())
    transformator = PictureTransformator()

    file_names = google_drive.get_file_list(google_drive_dir)
    for k, v in file_names.items():
        file_name, file_id = k, v
        print(file_name, file_id)
        if transformator.is_proper_image(file_name):
            google_drive.download_file(file_id, file_name, save_local_dir)
        # google_drive.delete_file(file_id)


def optimize_pictures(raw_dir, compressed_dir):
    transformator = PictureTransformator(rename=True)
    for file in os.listdir(raw_dir):
        transformator.compress(file, raw_dir, compressed_dir)


def main():
    # delete the file token.pickle after modifying the SCOPE
    # SCOPES = ['https://www.googleapis.com/auth/drive']
    cwd = os.getcwd()
    temp_path = os.path.join(cwd, 'temp')
    raw_local_dir = os.path.join(temp_path, 'raw')
    compressed_local_dir = os.path.join(temp_path, 'compressed')

    # get_pictures_from_google(cwd, SCOPES, "Jaskowe", raw_local_dir)
    optimize_pictures(raw_local_dir, compressed_local_dir)


if __name__ == '__main__':
    main()
