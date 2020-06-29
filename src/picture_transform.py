from PIL import Image
import os.path
import ffmpeg


class PictureTransformator:

    def __init__(self, rename=False, counter=0):
        self.rename = rename
        if counter >= 0:
            self.counter = counter
        else:
            self.counter = 0

    def is_proper_image(self, filename):
        try:
            i = filename.lower().split(".")[1]
            return i in ("jpg", "jpeg")
        except IndexError:
            return False

    def compress_image(self, file_to_compress, new_file):
        try:
            img = Image.open(file_to_compress)
            img.save(
                    new_file,
                    optimize=True,
                    progressive=True
                )
            return True
        except IOError:
            return False

    def compress_video(self, file_to_compress, new_file):
        print(new_file)
        (
            ffmpeg
            .input(file_to_compress)
            .output(new_file, vcodec="h264", acodec="mp3")
            .run()
        )
        return True

    def compress(self, file_name, raw_dir, compressed_dir):
        if self.rename:
            new_file_name = self.rename_to_date_numeral(file_name)
        else:
            new_file_name = file_name
        file_to_compress = os.path.join(raw_dir, file_name)
        file_to_save = os.path.join(compressed_dir, new_file_name)
        ext = file_name.split(".")[1].lower()
        if ext == "jpg":
            return self.compress_image(file_to_compress, file_to_save)
        elif ext == "mp4":
            return self.compress_video(file_to_compress, file_to_save)
        return False

    def rename_to_date_numeral(self, old_name):
        try:
            if old_name[4] == "-" and \
                    old_name[7] == "-" and \
                    old_name[10] == "_":
                return old_name
            splat = ""
            if old_name[0:3] in ("IMG", "VID"):
                splat = old_name.lower().split("_")[1]
            elif old_name[0:3] == "ima":
                splat = old_name.lower().split("-")[1]

            year = splat[0:4]
            month = splat[4:6]
            day = splat[6:8]
            ext = old_name.split(".")[1]
            self.counter += 1
            return f"{year}-{month}-{day}_c{self.counter}.{ext}"
        except IndexError:
            return old_name
