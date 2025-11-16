from pydantic import BaseModel
from random import choice
import numpy as np
from random import shuffle


class KeySequence(BaseModel):
    sequence: list[tuple[str, str]]


class Omission(BaseModel):
    matrix: str
    row: int
    col: int


class MultiplicationResponse(BaseModel):
    a: list[list[float]]
    b: list[list[float]]
    c: list[list[float]]
    omissions: list[Omission]
    valid: bool
    detail: str


def validate_omission(mat, row, col):
    if row < len(mat) and col < len(mat[0]):
        return True
    return False


def generate_key_presses(mat, row, col):
    x = mat[row][col]
    omitted_value = str(int(x) if x.is_integer() else float(x))
    sequence = []
    blank = "_" * len(omitted_value)
    for i, c in enumerate(omitted_value):
        blank = blank[:i] + c + blank[i + 1 :]
        sequence.append((c, blank))
    return sequence


def create_multiplication_problem(a, b, c, num_omissions, omit_from="c"):
    res = MultiplicationResponse(a=a, b=b, c=c, omissions=[], valid=False, detail="")

    if omit_from not in ["a", "b", "c"]:
        res.detail = "omit_from must be one of 'a', 'b', or 'c', got " + omit_from
        return res

    if not np.array_equal(c, a @ b):
        res.detail = f"{c} != {a} @ {b}, bad inner product attempt"
        return res

    omissions = []

    if omit_from == "a":

        if num_omissions > len(a):
            res.detail = (
                "max number omissions for left matrix must <= the number of rows"
            )
            return res
        if np.linalg.matrix_rank(b) != len(b[0]):
            # for a unique solution, b must have full column rank
            res.detail = "b must have full column rank, for a unique solution"
            return res

        omissions = [
            Omission(matrix="a", row=i, col=j)
            for i, j in row_wise_omit(a, num_omissions)
        ]

    elif omit_from == "b":

        if num_omissions > len(b):
            res.detail = (
                "max number omissions for right matrix must <= the number of columns"
            )
            return res

        if np.linalg.matrix_rank(a) != len(a):
            res.detail = "a must have full row rank, for a unique solution"
            return res

        omissions = [
            Omission(matrix="b", row=i, col=j)
            for i, j in column_wise_omit(b, num_omissions)
        ]

    elif omit_from == "c":
        num_cells = len(c[0]) * len(c)
        if num_omissions > num_cells:
            res.detail = f"max number omissions from product matrix must <= the number of cells in c. got {num_omissions}, want <= {num_cells}"
        omissions = [
            Omission(matrix="c", row=i, col=j)
            for i, j in cell_wise_omit(c, num_omissions)
        ]

    res.omissions = omissions
    res.valid = True
    res.detail = "ok"
    return res


def row_wise_omit(m, num_omissions):
    omissions = []
    c = list(enumerate(m))
    shuffle(c)
    k = 0
    while len(c) and k < num_omissions:
        i, row = c.pop()
        j = choice(range(len(row)))
        omissions.append((i, j))
        k += 1
    return omissions


def column_wise_omit(m, num_omissions):
    omissions = row_wise_omit(np.array(m).T.tolist(), num_omissions)
    return [(j, i) for i, j in omissions]


def cell_wise_omit(m, num_omissions):
    flat = []
    for i, row in enumerate(m):
        for j, _ in enumerate(row):
            flat.append((i, j))
    shuffle(flat)
    return flat[:num_omissions]
