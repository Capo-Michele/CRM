from fastapi import FastAPI

from app.api.auth import router as auth_router

app = FastAPI(
    title="CRM API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "project": "CRM v2"
    }


app.include_router(auth_router)