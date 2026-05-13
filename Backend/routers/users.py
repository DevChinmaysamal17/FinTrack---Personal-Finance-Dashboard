from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from Backend.database import engine
from Backend import models, oauth2
from Backend.hashing import Hash
from Backend.dependencies import get_db
from Backend.schemas import (
    UserCreate,
    UserResponse,
)
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse, tags=["Users"])
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = Hash.bcrypt(request.password)
    user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    default_categories = [
        {"name": "Salary",        "type": "income"},
        {"name": "Business",      "type": "income"},
        {"name": "Other Income",  "type": "income"},
        {"name": "Food",          "type": "expense"},
        {"name": "Rent",          "type": "expense"},
        {"name": "Transport",     "type": "expense"},
        {"name": "Shopping",      "type": "expense"},
        {"name": "Health",        "type": "expense"},
        {"name": "Entertainment", "type": "expense"},
        {"name": "Education",     "type": "expense"},
        {"name": "Other",         "type": "expense"},
    ]

    for cat in default_categories:
        new_cat = models.Category(
            name=cat["name"],
            category_type=cat["type"],
            user_id=user.id
        )
        db.add(new_cat)

    db.commit()
    return user


@router.delete("/{user_id}", tags=["Users"])
def destroy_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}