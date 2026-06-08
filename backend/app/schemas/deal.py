from decimal import Decimal

from pydantic import BaseModel
from enum import Enum

from app.models.enums import DealStatus

class DealCreate(BaseModel):
    title: str
    amount: Decimal

    company_id: int


class DealResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    status: DealStatus
    company_id: int

    class Config:
        from_attributes = True

class DealUpdate(BaseModel):
    title: str | None = None
    amount: Decimal | None = None
    status: DealStatus | None = None

class DealStatus(str, Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"

owner_id: int | None = None