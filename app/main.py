from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello from FastAPI"}


@app.get("/breathing")
def breathing():
    return {"message": "I'm OK. Thanks for checking 🥰"}
