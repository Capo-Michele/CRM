from pydantic import BaseModel


class ContactCreate(BaseModel):
    first_name: str
    last_name: str

    email: str | None = None
    phone: str | None = None

    position: str | None = None

    company_id: int


class ContactResponse(BaseModel):
    id: int

    first_name: str
    last_name: str

    email: str | None = None
    phone: str | None = None

    position: str | None = None

    company_id: int

    class Config:
        from_attributes = True