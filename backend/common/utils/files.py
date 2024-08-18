import os


def is_path_exists(path: str) -> bool:
    """
    Checks if the specified path exists.

    Parameters
    ----------
    path: str
        path

    Returns
    -------
    result of checking
    """
    return os.path.exists(path)


def make_dir(path: str) -> None:
    """
    Create specified directory recursively.

    if the specified directory does not exist, it will be created.

    Parameters
    ----------
    path
        directory path
    """
    if not is_path_exists(path):
        os.makedirs(path)
