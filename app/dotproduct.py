from pydantic import BaseModel
from random import choice


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


def choose_cell(m: MultiplicationResponse, matrices: list[str] = ["a", "b", "c"]):
    as_dict = m.model_dump()
    mat = choice(matrices)
    total_rows = len(as_dict[mat])
    total_cols = len(as_dict[mat][0])
    row = choice(range(total_rows))
    col = choice(range(total_cols))
    return Omission(matrix=mat, row=row, col=col)


def no_such_omission_already(omissions: list[Omission], omission: Omission):
    for o in omissions:
        if (
            o.matrix == omission.matrix
            and o.row == omission.row
            and o.col == omission.col
        ):
            return False
    return True


def create_mutltiplication_problem(
    a, b, c, num_omissions, can_omit_from=["a", "b", "c"]
):
    assert c == a @ b, f"{c} != {a} @ {b}"
    res = MultiplicationResponse(a=a, b=b, c=c, omissions=[])
    omissions = []
    tries = 0
    while len(omissions) < num_omissions and tries < 100:
        tries += 1
        omission = choose_cell(res, can_omit_from)
        if no_such_omission_already(omissions, omission):
            omissions.append(omission)
    return MultiplicationResponse(a=a, b=b, c=c, omissions=omissions)
