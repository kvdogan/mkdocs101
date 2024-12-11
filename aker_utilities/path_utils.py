import datetime
import os
from pathlib import Path


def checkfile(path: Path | str) -> Path:
    """
    Check file in the path, and extend with '(1)' like numbering system if there exists
    That helps to avoid overwriting and existing file.

    Args:
        path (Path | str): _description_

    Returns:
        Path: _description_
    """
    if isinstance(path, str):
        path = Path(path)

    path = Path(path).expanduser()

    if not path.exists():
        return path

    fname, ext = path.stem, path.suffix

    dir = path.parent

    ls = list(dir.iterdir())

    candidate = path
    index = 1
    while candidate in ls:
        candidate = Path(dir, f"{fname}({index}){ext}")
        index += 1

    return candidate


def get_folder_structure(path: str | Path, file_type: str | list[str] | None = None) -> dict:
    """
    Generates folder structure as a dictionary.

    Args:
        path (str | Path): _description_
        file_type (str | list[str] | None, optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """

    if isinstance(path, str):
        path = Path(path)

    if isinstance(file_type, list):
        file_type = [i.lower() for i in file_type]
        file_type = list(map(lambda x: x if x.startswith(".") else f".{x}", file_type))
    elif isinstance(file_type, str):
        file_type = file_type.lower()
        file_type = file_type if file_type.startswith(".") else f".{file_type}"
    elif file_type is None:
        pass

    basedir = path.name

    # Recursive function to generate folder structure
    def path_to_dict(path, d):
        name = path.name

        if path.is_dir():
            if name not in d:
                d[name] = {".": []}
            for x in os.listdir(path):
                path_to_dict(Path(path, x), d[name])
        else:
            if file_type is None or isinstance(file_type, str) and path.suffix == file_type:
                d["."].append(name)
            elif file_type is not None and isinstance(file_type, list) and path.suffix in file_type:
                d["."].append(name)
            else:
                pass

        return d

    structure = path_to_dict(path, {})

    return structure[basedir]


def get_filepaths(
    rootdir: str | Path,
    file_type: str | list[str] | None = None,
    flat: bool = True,
    recursive: bool = True,
) -> list[Path] | list[tuple[str, Path, int]]:
    """
    Advanced tool for getting file paths from nested folders.

    >>  In case of flat argument is True:
    >   ['file1_fullpath', 'file2_fullpath', ....]
    >   ['C:\\temp\\xxx.txt',r'C:\\temp\\temp2\\xxx.txt', ....]

    >>  In case of flat argument is False:
        Returns a list of tuples of filename, full path to folder and index in rootdir

    >   [(file1_name, file1_parentfolder_path, file1_peers_number)]
    >   [
            ("xxx.txt", r'C:\\temp', 2),
            ('xxx.txt',r'C:\\temp\\temp2',5)
        ]

    Args:
        rootdir (str | Path): Fullpath to directory, string, default is None.
        file_type (str | list[str], optional): File extension to look up, string or list,
                                               Defaults to None
        flat (bool, optional): Return either flat list consist of fullpath of files from
                               nested folders if 'flat' is True. Defaults to True.

    Raises:
        TypeError: _description_

    Returns:
        list[Path] | list[tuple[str, Path, int]]: _description_
    """
    if isinstance(rootdir, str):
        rootdir = Path(rootdir)

    if isinstance(file_type, list):
        file_type = [i.lower() for i in file_type]
        file_type = list(map(lambda x: x if x.startswith(".") else f".{x}", file_type))
    elif isinstance(file_type, str):
        file_type = file_type.lower()
        file_type = file_type if file_type.startswith(".") else f".{file_type}"
    elif file_type is None:
        pass
    else:
        raise TypeError("file_type argument must be either string, list or None")

    if file_type is None:
        file_paths = [
            (filename, Path(root))
            for root, directories, filenames in os.walk(rootdir)
            for filename in filenames
            if "$" not in filename
        ]
    else:
        file_paths = [
            (filename, Path(root))
            for root, directories, filenames in os.walk(rootdir)
            for filename in filenames
            # prevent fetching a filename without extension
            if Path(filename).suffix.lower() != ""
            # Comparing with "in" for string and list compatibility
            and Path(filename).suffix.lower() in file_type and "$" not in filename
        ]

    if not recursive:
        file_paths = [i for i in file_paths if i[1] == rootdir]

    if flat:
        return [Path(root, file) for file, root in file_paths]
    else:
        return [i + (file_paths.index(i) + 1,) for i in file_paths]


def is_file_created_within_given_margin(
    path: str | Path,
    margin_in_sec: int,
    reference_datetime: datetime.datetime | None = None,
    debug: bool = False,
) -> bool:
    """
    Check if the last edit date for a file is within given margin by the given reference.
    If no reference date is given, exact time being will be considered as reference time.
    Returns True or False

    Args:
        path (str | Path): [description]
        margin_in_sec (int): Allowed time difference in seconds
        reference_datetime (datetime.datetime, optional): [description]. Defaults to None.
        debug (bool, optional): Defaults to False. Prints timediff if needed.

    Returns:
        bool: [description]
    """
    if isinstance(path, str):
        path = Path(path)

    assert path.exists(), f"No such file: {path}"

    ctime = datetime.datetime.fromtimestamp(os.stat(path).st_ctime)

    if isinstance(reference_datetime, datetime.datetime):
        timediff = reference_datetime - ctime
    else:
        timediff = datetime.datetime.now() - ctime

    if debug:
        print(timediff)

    if timediff.total_seconds() <= margin_in_sec:
        return True
    else:
        return False
