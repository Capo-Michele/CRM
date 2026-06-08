from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate
from app.schemas.contact import ContactResponse


from app.services.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


@router.post(
    "",
    response_model=ContactResponse
)
def create_contact(
    data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = Contact(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        position=data.position,
        company_id=data.company_id,
        organization_id=current_user.organization_id
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact

@router.get(
    "",
    response_model=list[ContactResponse]
)
def get_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Contact)
        .filter(
            Contact.organization_id
            == current_user.organization_id
        )
        .all()
    )


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact = db.get(
        Contact,
        contact_id
    )

    if (
        not contact
        or contact.organization_id
        != current_user.organization_id
    ):
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    db.delete(contact)
    db.commit()

    return {
        "message": "Contact deleted"
    }