from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.companies import router as companies_router
from app.api.contacts import router as contacts_router
from app.api.deals import router as deals_router
from app.api.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(companies_router)
app.include_router(contacts_router)
app.include_router(deals_router)
app.include_router(dashboard_router)