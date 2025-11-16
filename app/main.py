from typing import Literal
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import HTMLResponse
import numpy as np
from pydantic import BaseModel
from app.dotproduct import MultiplicationResponse, create_multiplication_problem

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index():
    return "<body style='background-color:gold'><div class='smile' style='position:absolute;top:0;left:0;font-size:300px;pointer-events:none;'>😄</div><script>const s=document.querySelector('.smile');let x=0,y=0,mx=0,my=0;document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY});function a(){x+=(mx-x)*0.1;y+=(my-y)*0.1;s.style.transform=`translate(${x}px,${y}px)`;requestAnimationFrame(a)}a();</script></body>"


@app.get("/breathing")
async def breathing():
    return {"message": "I'm OK. Thanks for checking 🥰"}


class DotProductRequest(BaseModel):
    outer_dim_a: int
    inner_dim: int
    outer_dim_b: int
    num_omissions: int = 3
    omit_from: str


@app.post("/dotproduct")
async def dotproduct(request: DotProductRequest):
    num_attempts = 1000
    res = None
    for _ in range(num_attempts):
        a = np.random.randint(0, 10, size=(request.outer_dim_a, request.inner_dim))
        b = np.random.randint(0, 10, size=(request.outer_dim_b, request.inner_dim)).T
        c = a @ b
        res = create_multiplication_problem(
            a,
            b,
            c,
            request.num_omissions,
            request.omit_from,
        )
        if res.valid:
            break
    assert res is not None, "Failed to generate a valid multiplication problem"
    if res.valid:
        return res
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=res.detail,
        )
