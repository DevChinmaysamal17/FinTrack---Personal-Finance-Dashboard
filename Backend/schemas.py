from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    category_type: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    category_type: Literal["income", "expense"]

    class Config:
        from_attributes = True

class CategoryInTransaction(BaseModel):
    id: int
    name: str
 
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    amount: float
    type: str
    note: str | None = None
    date: datetime
    category_id: int

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    note: str | None
    date: datetime
    category_id: int
    user_id: int
    category: Optional[CategoryInTransaction] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class BudgetCreate(BaseModel):
    amount: float
    date: datetime
    category_id: int

class BudgetResponse(BaseModel):
    id: int
    amount: float
    date: datetime
    user_id: int
    category_id: int
    category: Optional[CategoryInTransaction] = None

    class Config:
        from_attributes = True