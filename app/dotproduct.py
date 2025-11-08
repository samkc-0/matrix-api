from os import wait
from fastapi import status
import numpy as np
from pydantic import BaseModel
from typing import Optional
from random import choice


class KeySequence(BaseModel):
    sequence: list[tuple[str, str]]


class Omission(BaseModel):
    matrix: str
    row: int
    col: int


class MultiplicationResponse(BaseModel):
    a: np.ndarray
    b: np.ndarray
    c: np.ndarray
    omissions: list[Omission]


def validate_omission(mat, row, col):
    if row < mat.shape[0] and col < mat.shape[1]:
        return True
    return False


def generate_key_presses(mat, row, col):
    x = mat[row][col]
    omitted_value = str(int(x) if x.is_integer() else x)
    sequence = []
    blank = "_" * len(omitted_value)
    for i, c in enumerate(omitted_value):
        blank = blank[:i] + c + blank[i + 1 :]
        sequence.append((c, blank))
        return sequence
