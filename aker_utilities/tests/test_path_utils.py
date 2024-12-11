import shutil
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from aker_utilities.path_utils import (
    checkfile,
    get_filepaths,
    get_folder_structure,
    is_file_created_within_given_margin,
)


# Session Based
@pytest.fixture(autouse=True, scope="session")
def setup(tmp_path_factory):
    TXT_CONTENT = "CONTENT"
    JSON_CONTENT = "{'test': 'CONTENT'}"

    root_folder = tmp_path_factory.mktemp("data")

    empty_folder = Path(root_folder, "empt_test_folder")
    empty_folder.mkdir(parents=True, exist_ok=True)

    sub_folder = Path(root_folder, "subfolder")
    sub_folder.mkdir(parents=True, exist_ok=True)

    sub_folder_sub = Path(sub_folder, "sub2")
    sub_folder_sub.mkdir(parents=True, exist_ok=True)

    f1 = Path(root_folder, "txtfileA.txt")
    f1.write_text(TXT_CONTENT)
    f2 = Path(root_folder, "txtfileA(1).txt")
    f2.write_text(TXT_CONTENT)
    f3 = Path(root_folder, "jsonfileA.json")
    f3.write_text(JSON_CONTENT)
    f4 = Path(sub_folder, "jsonfileB.json")
    f4.write_text(JSON_CONTENT)
    f5 = Path(sub_folder_sub, "mdfileB.md")
    f5.write_text(TXT_CONTENT)

    yield root_folder
    shutil.rmtree(root_folder.parent)


@pytest.mark.parametrize(
    "path,expected",
    [
        ("txtfileA.txt", "txtfileA(2).txt"),
        ("new_file.txt", "new_file.txt"),
        (Path("txtfileA.txt"), "txtfileA(2).txt"),
        (Path("new_file.txt"), "new_file.txt"),
    ],
)
def test_checkfile(path, expected, setup) -> None:
    path = str(Path(setup, path))
    assert checkfile(path) == Path(setup, expected)


@pytest.mark.parametrize(
    "file_type,flat,recursive, expected",
    [
        (".json", True, True, ["jsonfileA.json", "subfolder\\jsonfileB.json"]),
        (".json", True, False, ["jsonfileA.json"]),
        (
            None,
            True,
            True,
            [
                "jsonfileA.json",
                "txtfileA(1).txt",
                "txtfileA.txt",
                "subfolder\\jsonfileB.json",
                "subfolder\\sub2\\mdfileB.md",
            ],
        ),
        (None, True, False, ["jsonfileA.json", "txtfileA(1).txt", "txtfileA.txt"]),
    ],
)
def test_get_filepaths_return_flat(file_type, flat, recursive, expected, setup) -> None:
    # pytest.set_trace()
    files = get_filepaths(str(setup), file_type, flat, recursive)
    expected_outcome = list(map(lambda x: Path(setup, x), expected))
    assert files == expected_outcome


@pytest.mark.parametrize(
    "file_type,flat,recursive, expected",
    [
        (
            ["json", "md"],
            False,
            True,
            [
                ("jsonfileA.json", "", 1),
                ("jsonfileB.json", "subfolder", 2),
                ("mdfileB.md", "subfolder\\sub2", 3),
            ],
        ),
        ("json", False, False, [("jsonfileA.json", "", 1)]),
        (
            None,
            False,
            True,
            [
                ("jsonfileA.json", "", 1),
                ("txtfileA(1).txt", "", 2),
                ("txtfileA.txt", "", 3),
                ("jsonfileB.json", "subfolder", 4),
                ("mdfileB.md", "subfolder\\sub2", 5),
            ],
        ),
        (
            None,
            False,
            False,
            [
                ("jsonfileA.json", "", 1),
                ("txtfileA(1).txt", "", 2),
                ("txtfileA.txt", "", 3),
            ],
        ),
    ],
)
def test_get_filepaths_return_non_flat(
    file_type, flat, recursive, expected, setup
) -> None:
    # pytest.set_trace()
    files = get_filepaths(str(setup), file_type, flat, recursive)
    expected_outcome = list(map(lambda x: (x[0], Path(setup, x[1]), x[2]), expected))
    assert files == expected_outcome


def test_get_filepaths_raise_typeerror(setup) -> None:
    # pytest.set_trace()
    with pytest.raises(TypeError) as e_info:
        get_filepaths(str(setup), 123, True, False) # type: ignore


def test_get_folder_structure(setup):
    assert get_folder_structure(str(setup), file_type=None) == {
        ".": ["jsonfileA.json", "txtfileA(1).txt", "txtfileA.txt"],
        "empt_test_folder": {".": []},
        "subfolder": {".": ["jsonfileB.json"], "sub2": {".": ["mdfileB.md"]}},
    }


def test_get_folder_structure_json_files(setup):
    assert get_folder_structure(str(setup), file_type=".json") == {
        ".": ["jsonfileA.json"],
        "empt_test_folder": {".": []},
        "subfolder": {".": ["jsonfileB.json"], "sub2": {".": []}},
    }


def test_get_folder_structure_json_and_md_file(setup):
    assert get_folder_structure(str(setup), file_type=["json", "md"]) == {
        ".": ["jsonfileA.json"],
        "empt_test_folder": {".": []},
        "subfolder": {".": ["jsonfileB.json"], "sub2": {".": ["mdfileB.md"]}},
    }


@pytest.mark.parametrize(
    "filename,margin,reference_datetime,debug,expected",
    (
        ("txtfileA.txt", 1, None, True, True),
        ("txtfileA.txt", 1, datetime.now() + timedelta(hours=1), False, False),
    ),
)
def test_is_file_created_within_given_margin(
    filename, margin, reference_datetime, debug, expected, setup
):
    assert (
        is_file_created_within_given_margin(
            str(Path(setup, filename)), margin, reference_datetime, debug
        )
        == expected
    )
