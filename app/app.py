from fastapi import FastAPI
from routes.find import router as find_router

app = FastAPI()

app.include_router(find_router)
