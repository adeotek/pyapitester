import os


def get_full_path(input_path: str) -> str:
    if os.path.isabs(input_path):
        return input_path
    else:
        return os.path.join(os.getcwd(), input_path)
