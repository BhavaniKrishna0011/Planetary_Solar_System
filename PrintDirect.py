import os
from pathlib import Path

def list_files_os(directory_path):
    print("Listing files using os module:")
    try:
        with os.scandir(directory_path) as entries:
            for entry in entries:
                if entry.is_file():
                    print(entry.name)
    except FileNotFoundError as e:
        print(f"Error: {e}")

def list_files_pathlib(directory_path):
    print("Listing files using pathlib module:")
    try:
        directory_path = Path(directory_path)
        for file in directory_path.iterdir():
            if file.is_file():
                print(file.name)
    except FileNotFoundError as e:
        print(f"Error: {e}")

# Specify the directory path
directory_path = "."

# List files using os module
list_files_os(directory_path)

# List files using pathlib module
list_files_pathlib(directory_path)
