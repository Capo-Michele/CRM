from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.companies import router as companies_router
from app.api.contacts import router as contacts_router
from app.api.deals import router as deals_router

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
app.include_router(users_router)
app.include_router(companies_router)
app.include_router(contacts_router)
app.include_router(deals_router)