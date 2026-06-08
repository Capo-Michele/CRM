from decimal import Decimal

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Enum

from app.db.base import Base

from app.models.enums import DealStatus


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0
    )

    status: Mapped[DealStatus] = mapped_column(
        Enum(DealStatus),
        default=DealStatus.NEW
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id")
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id")
    )

    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    company = relationship(
        "Company",
        back_populates="deals"
    )

    owner = relationship("User")