from fastapi import status
from fastapi.testclient import TestClient
import numpy as np
import pytest

import app.dotproduct as dotproduct
from app.dotproduct import generate_key_presses


def dims(rows, cols):
    return dotproduct.Coordinate(row=rows, column=cols)


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
    assert generate_key_presses(a, 0, 0) == [("2", "2")]
    assert generate_key_presses(b, 1, 0) == [("4", "4__"), (".", "4._"), ("3", "4.3")]
    assert generate_key_presses(c, 0, 0) == [
        ("1", "____"),
        ("0", "10__"),
        (".", "10._"),
        ("6", "10.6"),
    ]
