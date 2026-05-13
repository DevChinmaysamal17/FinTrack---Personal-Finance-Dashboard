from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from Backend.database import engine
from Backend import models, oauth2
from Backend.dependencies import get_db
from Backend.schemas import (
    CategoryCreate,
    CategoryResponse,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=CategoryResponse)
def create_category(
    request: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    category = models.Category(
        **request.model_dump(),   
        user_id=current_user.id
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/", response_model=list[CategoryResponse])
def all_categories(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    return db.query(models.Category).filter(
        models.Category.user_id == current_user.id
    ).all()


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    request: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = request.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def destroy_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
