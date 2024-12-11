import csv
import json
import os
from itertools import chain
from pathlib import Path
from typing import Any

from deepdiff import DeepDiff
from ruamel.yaml import YAML

from aker_utilities.path_utils import checkfile


def json_to_csv(
    input_file_path: os.PathLike, output_file_path: os.PathLike, sep: str = ";"
) -> None:
    """
    _summary_

    Args:
        input_file_path (os.PathLike): Full path to input json file. Json objects must be array
        output_file_path (os.PathLike): Full path to output csv file
        sep (str, optional): Delimiter, Defaults to ';'

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """
    from six import string_types

    def json_to_dicts(json_str) -> list[dict[str, Any]]:
        try:
            objects = json.loads(json_str)
        except json.decoder.JSONDecodeError:
            objects = [json.loads(line) for line in json_str.split("\n") if line.strip()]

        if not isinstance(objects, list):
            raise TypeError("Top level of JSON document must be an array")

        return [dict(to_keyvalue_pairs(obj)) for obj in objects]

    def to_keyvalue_pairs(source, ancestors=[], key_delimeter: str = "_"):
        def is_sequence(arg) -> bool:
            return (not isinstance(arg, string_types)) and (
                hasattr(arg, "__getitem__") or hasattr(arg, "__iter__")
            )

        def is_dict(arg) -> bool:
            return isinstance(arg, dict)

        if is_dict(source):
            result = [
                to_keyvalue_pairs(source[key], ancestors + [key]) for key in source.keys()
            ]
            return list(chain.from_iterable(result))
        elif is_sequence(source):
            result = [
                to_keyvalue_pairs(item, ancestors + [str(index)])
                for (index, item) in enumerate(source)
            ]
            return list(chain.from_iterable(result))
        else:
            return [(key_delimeter.join(ancestors), source)]

    def dicts_to_csv(source, output_file, sep):
        from six import string_types

        def build_row(dict_obj, keys):
            return [dict_obj.get(k, "") for k in keys]

        keys = sorted(set(chain.from_iterable([o.keys() for o in source])))
        rows = [build_row(d, keys) for d in source]

        cw = csv.writer(output_file, delimiter=sep, lineterminator="\n")
        cw.writerow(keys)
        for row in rows:
            cw.writerow([c if isinstance(c, string_types) else c for c in row])

    with open(input_file_path) as input_file:
        json_file = input_file.read()
    dicts = json_to_dicts(json_file)
    with open(output_file_path, "w") as output_file:
        dicts_to_csv(dicts, output_file, sep)


def read_csv_to_lol(full_path: os.PathLike, sep: str = ";") -> list[list[str]]:
    """
    Read csv file into lists of list. Make sure to have a empty line at the bottom

    Args:
        full_path (os.PathLike): Full path to csv file
        sep (str, optional): Seperator string. Defaults to ";".

    Returns:
        list[list[str]]:
    """
    with open(full_path, "r") as ff:
        # read from CSV
        data = ff.readlines()
    # New line at the end of each line is removed
    data = [i.replace("\n", "") for i in data]
    # Creating lists of list
    data = [i.split(sep) for i in data]
    return data


def write_lol_to_csv(
    output_csv: os.PathLike,
    data: list[Any],
    headers: list[Any] | None = None,
    seperator: str = ";",
) -> None:
    if not isinstance(data, list) or not isinstance(headers, list | None):
        raise (TypeError("Data must be lists of list and header must be plain list"))

    if headers is not None and len(headers) != len(data[0]):
        raise (ValueError("Header and data length mismatch"))

    with open(output_csv, "w", newline="", encoding="utf-8") as output:
        csv_output = csv.writer(output, delimiter=seperator)
        if headers is not None:
            csv_output.writerow(headers)
        csv_output.writerows(data)


def write_list_to_txt(source_list: list | tuple, full_path_txt: os.PathLike) -> None:
    """
    _summary_

    Args:
        source_list (list): _description_
        full_path_txt (os.PathLike): _description_
    """
    if isinstance(source_list, list) or isinstance(source_list, tuple):
        with open(full_path_txt, "w") as ff:
            for i in source_list:
                ff.write("{}\n".format(i))
    else:
        raise (TypeError("Please use a python list for write into txt file"))


def read_from_txt(file_path: os.PathLike) -> list[Any]:
    """Read txt file_path as a list, each line becomes list item."""
    readings = []
    with open(file_path, "r") as ff:
        for i in ff.readlines():
            readings.append(i.replace("\n", ""))
    return readings


def combine_txt_files(
    folder: os.PathLike, sep: str = "\t", encoding: str = "latin1", skip_rows: int = 0
) -> None:
    """
    Combine txt files in a folder into one file, first column is written as file name.

    Args:
        folder (os.PathLike): Path to folder of files
        sep (str, optional): Separator for reading
        encoding (str, optional): Encoding of files.
        skip_rows (int, optional): Skiprows in header repeats in each file.
    """
    # Files only in folder, do not fetch files in subfolders.
    files = [i for i in Path(folder).glob("*") if i.is_file()]
    with open("Combined_output.txt", "a", encoding="latin1") as output:
        for file in files:
            with open(file, "r", encoding="latin1") as source:
                lines = source.readlines()
                for line in lines[skip_rows:]:
                    output.writelines(source.name + "\t" + line)


def write_dict_to_yaml(
    source_dict: dict,
    export_path: os.PathLike,
    mapping: int = 2,
    sequence: int = 4,
    offset: int = 2,
) -> None:
    """
    __summary__

    Args:
        source_dict (dict): Python dict to export to yaml file.
        export_path (str): Export path to create file
        mapping (int, optional): Whitespace number before dict items. Defaults to 2.
        sequence (int, optional): Whitespace number before the key of list item
                                  (min: offset + 2 is default). Defaults to 4.
        offset (int, optional): Whitespace number before "dash(-)" of list item.
                                Defaults to 2.
    """

    yaml = YAML()

    yaml.indent(mapping=mapping, sequence=sequence, offset=offset)

    with open(export_path, "w") as ff:
        yaml.dump(source_dict, ff)


def compare_data_structures(
    base: tuple[str, dict[Any, Any] | list],
    reference: tuple[str, dict[Any, Any] | list],
    output_folder: Path | None = None,
    **kwargs: dict[str, Any],
) -> DeepDiff:
    """
    _summary_

    Args:
        base (tuple[str, dict[str, Any]  |  list]):
            Tuple of dataset name and data structure either one of dictionary or list
        reference (tuple[str, dict[str, Any]  |  list]):
            Tuple of dataset name and data structure either one of dictionary or list
        output_folder (Path | None, optional): Path to export folder. Defaults to None.
        kwargs (dict[str, Any]):
            Additional arguments to pass to DD i.e. ignore_type_in_groups=[(str, int)]

    Raises:
        TypeError: _description_
        TypeError: _description_
        AssertionError: _description_

    Returns:
        DeepDiff: DeepDiff dictionary in any case
    """
    base_name, base_dataset = base
    ref_name, reference_dataset = reference

    if not isinstance(base_dataset, type(reference_dataset)):
        raise TypeError("Both datasets must be of the same type")

    # Overall assertion
    if isinstance(base_dataset, list) and isinstance(reference_dataset, list):
        base_dataset = sorted(base_dataset, key=str.casefold)
        reference_dataset = sorted(reference_dataset, key=str.casefold)

        if base_dataset == reference_dataset:
            return DeepDiff({}, {})
        else:
            diff = DeepDiff(base_dataset, reference_dataset, zip_ordered_iterables=True)

    elif isinstance(base_dataset, dict) and isinstance(reference_dataset, dict):
        if base_dataset != reference_dataset:
            diff = DeepDiff(base_dataset, reference_dataset, **kwargs)

        # PrettyOrderedSet is not json serializable hence casting list for serialization
        # for key, value in diff.items():
        #     if isinstance(value, PrettyOrderedSet):
        #         diff[key] = list(value)

        else:
            diff = DeepDiff({}, {})

    else:
        raise TypeError("Both datasets must be of type list or dict")

    if output_folder is not None:
        try:
            assert output_folder.is_dir()
            output_folder.mkdir(parents=True, exist_ok=True)
        except AssertionError:
            raise AssertionError("Please provide a valid directory path to export")

        export_path = checkfile(Path(output_folder, f"{base_name}_vs_{ref_name}.jsonc"))

        export_path.parent.mkdir(parents=True, exist_ok=True)

        with open(export_path, "a") as ff:
            ff.write("// Removed: Fields and/or tables are missing in new\n")
            ff.write("// Added: Fields and/or tables are missing in old\n")
            ff.write(f"// Old: {base_name} - New: {ref_name}\n")
            ff.write(diff.to_json(indent=4))

    return diff
