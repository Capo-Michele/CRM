from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate
from app.schemas.company import CompanyResponse
from app.schemas.company import CompanyUpdate
from fastapi import HTTPException
from app.services.auth import get_current_user
from app.models.user import User
from app.models.contact import Contact
from app.schemas.contact import ContactResponse
from app.models.deal import Deal
from app.schemas.deal import DealResponse

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.post(
    "",
    response_model=CompanyResponse
)
def create_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    company = Company(
        name=data.name,
        website=data.website,
        email=data.email,
        phone=data.phone,

        organization_id=current_user.organization_id
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

@router.get(
    "",
    response_model=list[CompanyResponse]
)
def get_companies(
    skip: int = 0,
    limit: int = 20,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = (
        db.query(Company)
        .filter(
            Company.organization_id
            == current_user.organization_id
        )
    )

    if search:
        query = query.filter(
            Company.name.ilike(f"%{search}%")
        )

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.get(
    "/{company_id}",
    response_model=CompanyResponse
)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.get(
        Company,
        company_id
    )

    if (
        not company
        or company.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


@router.delete(
    "/{company_id}"
)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.get(
        Company,
        company_id
    )

    if (
        not company
        or company.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    db.delete(company)
    db.commit()

    return {
        "message": "Company deleted"
    }


@router.patch(
    "/{company_id}",
    response_model=CompanyResponse
)
def update_company(
    company_id: int,
    data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.get(
        Company,
        company_id
    )

    if (
        not company
        or company.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():
        setattr(
            company,
            key,
            value
        )

    db.commit()
    db.refresh(company)

    return company

@router.get(
    "/{company_id}/contacts",
    response_model=list[ContactResponse]
)
def get_company_contacts(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.get(
        Company,
        company_id
    )

    if (
        not company
        or company.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return (
        db.query(Contact)
        .filter(
            Contact.company_id == company_id,
            Contact.organization_id
            == current_user.organization_id
        )
        .all()
    )


@router.get(
    "/{company_id}/deals",
    response_model=list[DealResponse]
)
def get_company_deals(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.get(
        Company,
        company_id
    )

    if (
        not company
        or company.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return (
        db.query(Deal)
        .filter(
            Deal.company_id == company_id,
            Deal.organization_id
            == current_user.organization_id
        )
        .all()
    )