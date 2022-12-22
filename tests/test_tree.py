import pytest

from tree import TreeStore


@pytest.fixture()
def items():
    return [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]


def test_get_all(items):
    ts = TreeStore(items)
    assert ts.get_all() == items


def test_get_item(items):
    ts = TreeStore(items)
    assert ts.get_item(1) == items[0]
    assert ts.get_item(2) == items[1]
    assert ts.get_item(7) == items[6]
    assert ts.get_item(8) == items[7]


def test_get_children(items):
    ts = TreeStore(items)
    assert ts.get_children(1) == [items[1], items[2]]


def test_get_children_if_they_not_exist(items):
    ts = TreeStore(items)
    assert ts.get_children(5) == []


def test_get_all_parents(items):
    ts = TreeStore(items)
    assert ts.get_all_parents(7) == [items[3], items[1], items[0]]
    assert ts.get_all_parents(8) == [items[3], items[1], items[0]]
    assert ts.get_all_parents(3) == [items[0]]