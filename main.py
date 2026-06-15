import logging

import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="News API",
    version="0.1.0",
)

@app.get("/", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}

def run() -> None:
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
