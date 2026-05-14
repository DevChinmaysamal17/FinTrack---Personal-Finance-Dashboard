from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session, joinedload
from Backend.database import engine
from Backend import models, oauth2
from Backend.dependencies import get_db
from Backend.schemas import (
    TransactionCreate,
    TransactionResponse,
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

# Creating a new transaction for a particular user 
@router.post("/", response_model=TransactionResponse)
def create_transaction(
    request: TransactionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    transaction = models.Transaction(
        **request.model_dump(),   
        user_id=current_user.id
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    transaction = db.query(models.Transaction).options(
        joinedload(models.Transaction.category)
    ).filter(models.Transaction.id == transaction.id).first()

    return transaction

# Get all transactions of that particular user
@router.get("/", response_model=list[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    return (
        db.query(models.Transaction)
        .options(joinedload(models.Transaction.category))
        .filter(models.Transaction.user_id == current_user.id)
        .order_by(models.Transaction.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

# Updating a transactions of that particular user
@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    request: TransactionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return transaction

# Deleting a transactions of that particular user
@router.delete("/{transaction_id}", tags=["Transactions"])
def destroy_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}