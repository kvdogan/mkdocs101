from collections import defaultdict
import re
from typing import Any, TextIO


##########################################################################################
# ## Algorithms for sorting & Hierarchical Structures
##########################################################################################

def hierarchy_tree(
    table: list[tuple[Any, Any]], visualize: bool = False, output_file: str | None = None
) -> dict[Any, Any] | None:
    """
    Creates a dictionary to represent hierarchical data

    Args:
        table (list[tuple[Any, Any]]): _description_
        visualize (bool, optional): _description_. Defaults to False.
        output_file (str | None, optional): _description_. Defaults to None.

    Returns:
        dict[Any, Any] | None: _description_

    Examples:
    >>> hierarchy_tree(
    ...     table=[
    ...         (22, 4), (45, 1), (1, 1), (4, 4), (566, 45), (7, 7), (66, 1),
    ...         (300, 8), (8, 4), (101, 7), (80, 22), (17, 17), (911, 66)
    ...     ]
    ... )
    {1: {66, 45}, 4: {8, 22}, 7: {101}, 8: {300}, 22: {80}, 45: {566}, 66: {911}}

    """
    nodes, roots = defaultdict(set), set()

    for child, parent in table:
        if child == parent:
            roots.add(child)
        else:
            nodes[parent].add(child)

    def print_on_screen(item: str, nodes: dict, level: int) -> None:
        print("\t" * level, f"\\_{item}")
        for child in sorted(nodes.get(item, [])):
            print_on_screen(child, nodes, level + 1)

    def write_to_file(item: str, nodes: dict, level: int, ff: TextIO) -> None:
        gap = "\t"
        ff.writelines(f"{gap * level} \\_{item}\n")
        for child in sorted(nodes.get(item, [])):
            write_to_file(child, nodes, level + 1, ff)

    if visualize:
        if output_file is None:
            for item in sorted(roots):
                print_on_screen(item, nodes, 0)
        else:
            with open(output_file, "w", encoding="utf-8") as ff:
                for item in sorted(roots):
                    write_to_file(item, nodes, 0, ff)
    else:
        return dict(sorted(nodes.items()))


def natural_sorted(alphanum_list: list) -> list:
    """
    When you try to sort a list of strings that contain numbers,
    the normal python sort algorithm sorts lexicographically,
    so you might not get the results that you expect.

    Code is taken from: https://stackoverflow.com/questions/4836710/

    Args:
        alphanum_list (list): _description_

    Returns:
        list: _description_


    Examples:

    >>> sorted(['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in'])
    ['1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '2 ft 7 in', '7 ft 6 in']

    >>> natural_sorted(['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 f 6 in'])
    ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 f 6 in', '10 ft 2 in']

    """
    def convert(text: str) -> int | str:
        if text.isdigit():
            return int(text)
        else:
            return text

    def create_alphanum_key(key: str) -> list:
        return [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(alphanum_list, key=create_alphanum_key)


def sorted_dict(d: dict, reverse: bool = False) -> dict:
    """
    Sorts a dictionary by its keys

    Args:
        d (dict): _description_
        reverse (bool, optional): _description_. Defaults to False.

    Returns:
        dict: _description_

    Examples:
    >>> sorted_dict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
    {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    >>> sorted_dict({'a': 1, 'b': 2, 'c': 3, 'd': 4}, reverse=True)
    {'d': 4, 'c': 3, 'b': 2, 'a': 1}

    """
    return dict(sorted(d.items(), key=lambda x: x[0], reverse=reverse))
