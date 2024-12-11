import json
from pathlib import Path

import pytest

from aker_utilities import IO_utils

JSON_SAMPLE_1 = [
    {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com",
        "isActive": True,
        "roles": ["admin", "user"],
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345",
        },
    },
    {
        "name": "Jane Doe",
        "age": 25,
        "email": "janedoe@example.com",
        "isActive": False,
        "roles": ["user"],
        "address": {
            "street": "456 Elm St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345",
        },
    },
]

JSON_SAMPLE_2 = {
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@example.com",
    "isActive": True,
    "roles": ["admin", "user"],
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
    },
}

DICT_SAMPLE_1 = {
    "John Doe": {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com",
        "isActive": True,
        "roles": ["admin", "user"],
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345",
        },
    },
    "Jane Doe": {
        "name": "Jane Doe",
        "age": 25,
        "email": "janedoe@example.com",
        "isActive": False,
        "roles": ["user"],
        "address": {
            "street": "456 Elm St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345",
        },
    },
}

DICT_SAMPLE_2 = {
    "John Doe": {
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com",
        "isActive": True,
        "roles": [
            "admin",
        ],
        "address": {
            "street": "456 Main St",
            "city": "Sometown",
            "state": "CA",
            "zip": "XXXXX",
        },
    }
}

LIST_SAMPLE_1 = ["John Doe", "Jane", "John Smith"]
LIST_SAMPLE_2 = ["Jane Doe", "John Smith"]

LOL_SAMPLE = [
    [
        "address_city",
        "address_state",
        "address_street",
        "address_zip",
        "age",
        "email",
        "isActive",
        "name",
        "roles_0",
        "roles_1",
    ],
    [
        "Anytown",
        "CA",
        "123 Main St",
        "12345",
        "30",
        "johndoe@example.com",
        "True",
        "John Doe",
        "admin",
        "user",
    ],
    [
        "Anytown",
        "CA",
        "456 Elm St",
        "12345",
        "25",
        "janedoe@example.com",
        "False",
        "Jane Doe",
        "user",
        "",
    ],
]


TEST_FOLDER = Path("__ref", "io_utils")
JSON_PATH_1 = Path(TEST_FOLDER, "sample_json_1.json")
JSON_PATH_2 = Path(TEST_FOLDER, "sample_json_2.json")
CSV_PATH = Path(TEST_FOLDER, "sample_csv.csv")


def test_write_files_for_testing() -> None:
    TEST_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(JSON_PATH_1, "w") as f:
        json.dump(JSON_SAMPLE_1, f)

    with open(JSON_PATH_2, "w") as f:
        json.dump(JSON_SAMPLE_2, f)


def test_json_to_csv() -> None:
    IO_utils.json_to_csv(
        input_file_path=JSON_PATH_1,
        output_file_path=CSV_PATH,
    )

    with open(CSV_PATH, "r") as f:
        lines = f.readlines()
        assert lines[0] == (
            "address_city;address_state;address_street;address_zip;age;email;"
            "isActive;name;roles_0;roles_1\n"
        )
        assert lines[1] == (
            "Anytown;CA;123 Main St;12345;30;johndoe@example.com;True;"
            "John Doe;admin;user\n"
        )
        assert lines[2] == (
            "Anytown;CA;456 Elm St;12345;25;janedoe@example.com;False;" "Jane Doe;user;\n"
        )


def test_json_to_csv_type_error() -> None:
    with pytest.raises(TypeError):
        IO_utils.json_to_csv(
            input_file_path=JSON_PATH_2,
            output_file_path=CSV_PATH,
        )


def test_write_lol_to_csv_type_error() -> None:
    with pytest.raises(TypeError):
        IO_utils.write_lol_to_csv(
            output_csv=CSV_PATH,
            headers="no header test; no header test",
            data=LOL_SAMPLE,
        )


def test_write_lol_to_csv_value_error() -> None:
    with pytest.raises(ValueError):
        IO_utils.write_lol_to_csv(
            output_csv=CSV_PATH,
            headers=LOL_SAMPLE[0][:-1],
            data=LOL_SAMPLE[1],
        )


def test_write_lol_to_csv() -> None:
    IO_utils.write_lol_to_csv(
        output_csv=CSV_PATH,
        # headers=LOL_SAMPLE[0],
        data=LOL_SAMPLE,
    )

    assert CSV_PATH.exists()


def test_read_csv_to_lol() -> None:
    test_write_lol_to_csv()
    sample_csv = IO_utils.read_csv_to_lol(CSV_PATH)

    assert sample_csv == [['address_city', 'address_state', 'address_street', 'address_zip', 'age', 'email', 'isActive', 'name', 'roles_0', 'roles_1'], ['Anytown', 'CA', '123 Main St', '12345', '30', 'johndoe@example.com', 'True', 'John Doe', 'admin', 'user'], ['Anytown', 'CA', '456 Elm St', '12345', '25', 'janedoe@example.com', 'False', 'Jane Doe', 'user', '']]


def test_compare_data_structures_type_error() -> None:
    with pytest.raises(TypeError):
        IO_utils.compare_data_structures(
            base=("Base", DICT_SAMPLE_1),
            reference=("Reference", LIST_SAMPLE_1),
        )


def test_write_dict_to_yaml() -> None:
    IO_utils.write_dict_to_yaml(
        source_dict=DICT_SAMPLE_1,
        export_path=Path(TEST_FOLDER, "sample_dict.yaml"),
    )

    with open(Path(TEST_FOLDER, "sample_dict.yaml"), "r") as f:
        assert f.read() == ("John Doe:\n  name: John Doe\n  age: 30\n  email: johndoe@example.com\n  isActive: true\n  roles:\n    - admin\n    - user\n  address:\n    street: 123 Main St\n    city: Anytown\n    state: CA\n    zip: '12345'\nJane Doe:\n  name: Jane Doe\n  age: 25\n  email: janedoe@example.com\n  isActive: false\n  roles:\n    - user\n  address:\n    street: 456 Elm St\n    city: Anytown\n    state: CA\n    zip: '12345'\n")

    Path(TEST_FOLDER, "sample_dict.yaml").unlink()


def test_compare_data_structures_type_error_tuple() -> None:
    with pytest.raises(TypeError):
        IO_utils.compare_data_structures(
            base=("Base", {1, 2, 3}),  # type: ignore
            reference=("Reference", {1, 2, 3}),  # type: ignore
        )


def test_compare_data_structures_dict() -> None:
    base = ("Base", DICT_SAMPLE_1)
    reference = ("Reference", DICT_SAMPLE_2)
    diff = IO_utils.compare_data_structures(base=base, reference=reference)

    assert diff.to_json() == (
        '{"dictionary_item_removed": ["root[\'Jane Doe\']"], '
        "\"values_changed\": {\"root['John Doe']['address']['street']\": "
        '{"new_value": "456 Main St", "old_value": "123 Main St"}, '
        "\"root['John Doe']['address']['city']\": {\"new_value\": \"Sometown\", "
        "\"old_value\": \"Anytown\"}, \"root['John Doe']['address']['zip']\": "
        '{"new_value": "XXXXX", "old_value": "12345"}}, "iterable_item_removed": '
        "{\"root['John Doe']['roles'][1]\": \"user\"}}"
    )


def test_compare_data_structures_iterable() -> None:
    base = ("Base", LIST_SAMPLE_1)
    reference = ("Reference", LIST_SAMPLE_2)
    diff = IO_utils.compare_data_structures(base=base, reference=reference)

    assert diff.to_json() == (
        '{"values_changed": {"root[0]": {"new_value": "Jane Doe", "old_value": "Jane"}, '
        '"root[1]": {"new_value": "John Smith", "old_value": "John Doe"}}, '
        '"iterable_item_removed": {"root[2]": "John Smith"}}'
    )


def test_remove_files_after_test_completion() -> None:
    for file in [JSON_PATH_1, JSON_PATH_2, CSV_PATH]:
        if file.exists():
            file.unlink()

    TEST_FOLDER.rmdir()


