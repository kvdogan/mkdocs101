from aker_utilities.algorithm_utils import hierarchy_tree, natural_sorted


def test_hierarchy_tree() -> None:
    assert hierarchy_tree(
        table=[
            (22, 4), (45, 1), (1, 1), (4, 4), (566, 45), (7, 7), (66, 1), (300, 8),
            (8, 4), (101, 7), (80, 22), (17, 17), (911, 66)
        ]
    ) == {1: {66, 45}, 4: {8, 22}, 7: {101}, 8: {300}, 22: {80}, 45: {566}, 66: {911}}


def test_natural_sorted() -> None:
    assert sorted(
        ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    ) == ['1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '2 ft 7 in', '7 ft 6 in']

    assert natural_sorted(
        ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 f 6 in']
    ) == ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 f 6 in', '10 ft 2 in']
