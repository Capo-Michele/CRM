from fastapi import APIRouter
from fastapi import Depends

from app.models.user import User
from app.schemas.user import UserResponse
from app.services.auth import get_current_user
from app.schemas.user import UserCreate
from app.services.auth import require_admin
from app.services.auth import hash_password
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post(
    "",
    response_model=UserResponse
)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
        organization_id=current_user.organization_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return (
        db.query(User)
        .filter(
            User.organization_id
            == current_user.organization_id
        )
        .all()
    )

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
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

    return user

@router.delete(
    "/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
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

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted"
    }

