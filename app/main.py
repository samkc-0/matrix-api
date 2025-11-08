from fastapi import FastAPI, status, HTTPException
import numpy as np

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello from FastAPI"}


@app.get("/breathing")
def breathing():
    return {"message": "I'm OK. Thanks for checking 🥰"}


@app.post("/dotproduct")
def dotproduct():
    return {"message": "not implemented"}
