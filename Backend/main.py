from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from Backend.database import engine
from Backend import models, oauth2
from Backend.hashing import Hash
from Backend.routers import auth
from Backend.dependencies import get_db
from Backend.schemas import (
    UserCreate,
    UserResponse,
    CategoryCreate,
    CategoryResponse,
    TransactionCreate,
    TransactionResponse,
    BudgetResponse,
    BudgetCreate
)


app = FastAPI()

# CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="Frontend"), name="static")
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)


# Serve Frontend
@app.get("/")
def serve_frontend():
    return FileResponse("Frontend/login.html")


# Users
@app.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(oauth2.get_current_user)):
    return current_user


@app.post("/users", response_model=UserResponse, tags=["Users"])
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


@app.delete("/users/{user_id}", tags=["Users"])
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


# Categories
@app.post("/categories", response_model=CategoryResponse, tags=["Categories"])
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


@app.get("/categories", response_model=list[CategoryResponse], tags=["Categories"])
def all_categories(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    return db.query(models.Category).filter(
        models.Category.user_id == current_user.id
    ).all()


@app.put("/categories/{category_id}", response_model=CategoryResponse, tags=["Categories"])
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


@app.delete("/categories/{category_id}", tags=["Categories"])
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


# Transactions 
@app.post("/transactions", response_model=TransactionResponse, tags=["Transactions"])
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


@app.get("/transactions", response_model=list[TransactionResponse], tags=["Transactions"])
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


@app.put("/transactions/{transaction_id}", response_model=TransactionResponse, tags=["Transactions"])
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


@app.delete("/transactions/{transaction_id}", tags=["Transactions"])
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

# Budget
@app.post("/budgets", response_model=BudgetResponse, tags=["Budgets"])
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


@app.get("/budgets", response_model=list[BudgetResponse], tags=["Budgets"])
def all_budget(
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    return (db.query(models.Budget)
            .options(joinedload(models.Budget.category)).
            filter(models.Budget.user_id == current_user.id)
            .all()
    )


@app.put("/budgets/{budget_id}", response_model=BudgetResponse, tags=["Budgets"])
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


@app.delete("/budgets/{budget_id}", tags=["Budgets"])
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

