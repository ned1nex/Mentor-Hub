from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import os
from dotenv import load_dotenv
from src import global_router

from core.config import config

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
app.include_router(global_router, prefix="/api")

allowed_domens = [
    "http://frontend",
    "http://frontend:3000",
    "http://localhost:3000",
    "http://localhost",
    "https://prod-team-30-mdmsvlv5.final.prodcontest.ru",  # Удалите слеш в конце
    "https://qdrant.prod-team-30-mdmsvlv5.final.prodcontest.ru"  # Добавьте субдомен qdrant
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_domens,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping", summary="Метод PING, проверка на работоспособность", tags=["Support"])
def ping():
    return {"status": f"Server is online, running on: {config.PORT} port."}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.PORT
    )