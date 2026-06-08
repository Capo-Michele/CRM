from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db

from app.models.company import Company
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.user import User
from app.models.enums import DealStatus

from app.services.auth import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organization_id = current_user.organization_id

    companies_count = (
        db.query(Company)
        .filter(
            Company.organization_id == organization_id
        )
        .count()
    )

    contacts_count = (
        db.query(Contact)
        .filter(
            Contact.organization_id == organization_id
        )
        .count()
    )

    deals_count = (
        db.query(Deal)
        .filter(
            Deal.organization_id == organization_id
        )
        .count()
    )

    revenue = (
    db.query(
        func.coalesce(
            func.sum(Deal.amount),
            0
        )
    )
    .filter(
        Deal.organization_id
        == organization_id
    )
    .scalar()
    )

    return {
    "companies": companies_count,
    "contacts": contacts_count,
    "deals": deals_count,
    "revenue": revenue
    }


@router.get("/pipeline")
def get_pipeline(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organization_id = current_user.organization_id

    result = {}

    for status in DealStatus:
        count = (
            db.query(Deal)
            .filter(
                Deal.organization_id == organization_id,
                Deal.status == status
            )
            .count()
        )

        result[status.value] = count

    return result

@router.get("/test")
def test():
    return {
        "companies": 1,
        "contacts": 2,
        "deals": 3,
        "revenue": 150000
    }