import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from config.settings import settings
from database.database import connect, disconnect
from routes.admin import router as admin_router
from routes.auth import router as auth_router
from routes.news import router as news_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect()
    yield
    await disconnect()

app = FastAPI(
    title="News API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(news_router)
app.include_router(admin_router)

@app.get("/", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}

def run() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
