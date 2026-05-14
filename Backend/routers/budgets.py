from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session, joinedload
from Backend.database import engine
from Backend import models, oauth2
from Backend.dependencies import get_db
from Backend.schemas import (
    BudgetResponse,
    BudgetCreate
)

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

# Creating a new budget 
@router.post("/", response_model=BudgetResponse)
def create_budget(
    request: BudgetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    budget = models.Budget(
        **request.model_dump(),   
        user_id=current_user.id
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

# All budgets
@router.get("/", response_model=list[BudgetResponse])
def all_budget(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    return (db.query(models.Budget)
            .options(joinedload(models.Budget.category)).
            filter(models.Budget.user_id == current_user.id)
            .all()
    )

# Updating a existing budget with id
@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: int,
    request: BudgetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == current_user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    budget.amount = request.amount
    budget.date = request.date
    budget.category_id = request.category_id
    db.commit()
    db.refresh(budget)
    return budget

# Deleting a budget 
@router.delete("/{budget_id}")
def destroy_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == current_user.id
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}