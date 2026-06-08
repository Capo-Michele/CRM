from fastapi import APIRouter, Depends

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.deal import Deal

from app.schemas.deal import (
    DealCreate,
    DealResponse,
    DealUpdate
)

from app.services.auth import get_current_user, require_admin
from app.models.user import User



router = APIRouter(
    prefix="/deals",
    tags=["Deals"]
)

@router.post( "", response_model=DealResponse )
def create_deal(
    data: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deal = Deal(
        title=data.title,
        amount=data.amount,

        company_id=data.company_id,

        organization_id=current_user.organization_id
    )

    db.add(deal)

    db.commit()
    db.refresh(deal)

    return deal

@router.get(
    "",
    response_model=list[DealResponse]
)
def get_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):
    return (
        db.query(Deal).filter(Deal.organization_id == current_user.organization_id).all())



@router.get(
    "/{deal_id}",
    response_model=DealResponse
)
def get_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deal = db.get(
        Deal,
        deal_id
    )
    if (
    not deal
    or deal.organization_id
    != current_user.organization_id
):
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )
    return deal


@router.patch(
    "/{deal_id}",
    response_model=DealResponse
)
def update_deal(
    deal_id: int,
    data: DealUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deal = db.get(
        Deal,
        deal_id
    )

    if (
    not deal
    or deal.organization_id
    != current_user.organization_id
):
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():
        setattr(
            deal,
            key,
            value
        )

    db.commit()
    db.refresh(deal)

    return deal


@router.delete( "/{deal_id}" )
def delete_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deal = db.get(
        Deal,
        deal_id
    )

    if ( not deal or deal.organization_id!= current_user.organization_id ):
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    db.delete(deal)
    db.commit()

    return {
        "message": "Deal deleted"
    }

@router.patch("/{deal_id}/assign/{user_id}")
def assign_deal(
    deal_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    deal = db.get(
        Deal,
        deal_id
    )

    if (
        not deal
        or deal.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Deal not found"
        )

    user = db.get(
        User,
        user_id
    )

    if (
        not user
        or user.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    deal.owner_id = user.id

    db.commit()
    db.refresh(deal)

    return {
        "message": "Deal assigned",
        "deal_id": deal.id,
        "owner_id": user.id
    }

@router.get(
    "/my",
    response_model=list[DealResponse]
)
def get_my_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Deal).filter(Deal.owner_id == current_user.id, Deal.organization_id == current_user.organization_id).all())