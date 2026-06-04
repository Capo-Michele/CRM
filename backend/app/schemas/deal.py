from decimal import Decimal

from pydantic import BaseModel


class DealCreate(BaseModel):
    title: str
    amount: Decimal

    company_id: int


class DealResponse(BaseModel):
    id: int

    title: str
    amount: Decimal

    status: str

    company_id: int

    class Config:
        from_attributes = True

class DealUpdate(BaseModel):
    title: str | None = None
    amount: Decimal | None = None
    status: str | None = None