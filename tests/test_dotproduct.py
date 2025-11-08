from fastapi import status
from fastapi.testclient import TestClient
import numpy as np
import pytest

from app.dotproduct import (
    MultiplicationResponse,
    generate_key_presses,
    choose_cell,
    validate_omission,
    create_mutltiplication_problem,
)


@pytest.fixture(scope="session", name="two_by_two")
def two_by_two():
    a = np.array([[1, 2]])
    b = np.array([[2], [4.3]])
    c = a @ b
    return a, b, c


def test_1x2_dot_2x1_key_sequence(two_by_two):
    a, b, c = two_by_two
    assert generate_key_presses(a, 0, 0) == [("1", "1")]
    assert generate_key_presses(a, 0, 1) == [("2", "2")]
    assert generate_key_presses(b, 0, 0) == [("2", "2")]
    assert generate_key_presses(b, 1, 0) == [("4", "4__"), (".", "4._"), ("3", "4.3")]
    assert generate_key_presses(c, 0, 0) == [
        ("1", "1___"),
        ("0", "10__"),
        (".", "10._"),
        ("6", "10.6"),
    ]


def test_choose_cell(two_by_two):
    a, b, c = two_by_two
    res = MultiplicationResponse(**{"a": a, "b": b, "c": c}, omissions=[])
    for _ in range(20):
        omission = choose_cell(res)
        m = omission.matrix
        r = omission.row
        c = omission.col
        assert validate_omission(res.model_dump()[m], r, c)


def test_create_mutltiplication_problem(two_by_two):
    a, b, c = two_by_two
    res = create_mutltiplication_problem(a, b, c, 2)
    assert len(res.omissions) == 2
    assert np.array(res.a) @ np.array(res.b) == np.array(res.c)
