import os
import shutil
import traceback
from pathlib import Path
import zipfile


class FileHelper:
    def remove_file(self, file_path):
        file_path = Path(file_path)
        try:
            os.remove(file_path)
        except FileNotFoundError as e:
            print("File {} doesn't exist!".format(file_path))
        except Exception as e:
            print("Error removing file_path '{}': {}".format(file_path, traceback.format_exc()))

    def move_file(self, src_path, dest_path):
        src_path = Path(src_path)
        dest_path = Path(dest_path)
        os.rename(src_path, dest_path)

    def create_directory(self, file_path):
        file_path = Path(file_path)
        os.makedirs(file_path)

    def remove_directory(self, file_path):
        file_path = Path(file_path)
        try:
            shutil.rmtree(file_path)
        except FileNotFoundError as e:
            print("File {} doesn't exist!".format(file_path))
        except Exception as e:
            print("Error removing directory '{}': {}".format(file_path, traceback.format_exc()))

    def recreate_directory(self, file_path):
        file_path = Path(file_path)
        self.remove_directory(file_path)
        self.create_directory(file_path)

    def create_zip(self, file_path, arcname, *files_to_archive):
        file_path = Path(file_path)
        zf = zipfile.ZipFile(file_path, mode='w')
        try:
            for file in files_to_archive:
                file = Path(file)
                zf.write(file, arcname=arcname)
                if file.is_dir():
                    for df in os.listdir(file):
                        zf.write("{}/{}".format(file, df), arcname="{}/{}".format(arcname, df))
                zf.printdir()

        finally:
            zf.close()

    def extract_all_zip(self, zip_src_path, extract_path):
        zip_src_path = Path(zip_src_path)
        extract_path = Path(extract_path)
        zf = zipfile.ZipFile(zip_src_path, mode='r')
        try:
            zf.extractall(path=extract_path)
        finally:
            zf.close()
