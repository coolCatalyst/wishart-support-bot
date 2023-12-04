import os

from constants import ALLOWED_FILES, dataset_folder

def clean_dataset(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(tuple(ALLOWED_FILES)):
                pass
            else:
                os.remove(os.path.join(root, file))

if __name__ == "__main__":
    clean_dataset(dataset_folder)