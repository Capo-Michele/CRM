from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    website: str | None = None
    email: str | None = None
    phone: str | None = None


class CompanyResponse(BaseModel):
    id: int
    name: str
    website: str | None = None
    email: str | None = None
    phone: str | None = None

    class Config:
        from_attributes = True

class CompanyUpdate(BaseModel):
    name: str | None = None
    website: str | None = None
    email: str | None = None
    phone: str | None = None