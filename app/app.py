from fastapi import FastAPI
from utils import greet

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": greet()}
