import os


def get_file(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'resources', name)
