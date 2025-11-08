from fastapi import FastAPI, status, HTTPException
import numpy as np
from pydantic import BaseModel
from app.dotproduct import create_multiplication_problem

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello from FastAPI"}


@app.get("/breathing")
def breathing():
    return {"message": "I'm OK. Thanks for checking 🥰"}


class DotProductRequest(BaseModel):
    outer_dim_a: int
    inner_dim: int
    outer_dim_b: int
    num_omissions: int = 3
    can_omit_from: list[str] = ["a", "b", "c"]


@app.post("/dotproduct")
def dotproduct(request: DotProductRequest):
    a = np.random.randint(0, 10, size=(request.outer_dim_a, request.inner_dim))
    b = np.random.randint(0, 10, size=(request.outer_dim_b, request.inner_dim)).T
    c = a @ b
    total_cells = (
        request.outer_dim_a * request.inner_dim
        + request.inner_dim * request.outer_dim_b
        + request.outer_dim_a * request.outer_dim_b
    )
    if request.num_omissions > total_cells:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="trying to omit more matrix cells than exist",
        )
    try:
        res = create_multiplication_problem(
            a=a,
            b=b,
            c=c,
            num_omissions=request.num_omissions,
            can_omit_from=request.can_omit_from,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return res
