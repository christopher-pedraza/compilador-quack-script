import pickle
import os
import sys


def read_and_delete_object_files(file_name):
    print(f"Reading object file: {file_name}")
    with open(file_name, "rb") as f:
        data = pickle.load(f)
        print(data)
    os.remove(file_name)


def translate_program(file_name):
    """
    Translates a QuackScript program from an object file
    """
    if not os.path.exists(file_name):
        print(f"File {file_name} does not exist.")
        return

    read_and_delete_object_files(file_name)


if __name__ == "__main__":
    read_and_delete_object_files()
