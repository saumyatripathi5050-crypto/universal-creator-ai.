main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Universal Creator AI Backend Active!"}
