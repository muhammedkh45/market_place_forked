from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AccountBase(BaseModel):
    email: str

class AccountCreate(AccountBase):
    password: str

class Account(AccountBase):
    id: int
    registration_date: datetime
    status: str
    is_active: bool
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    balance: float = 0.0

class UserCreate(UserBase):
    account: AccountCreate

class User(UserBase):
    id: int
    account: Account
    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    quantity: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    listed_date: datetime
    last_updated: datetime
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    quantity: int
    total_price: float
    status: str
    payment_method: str
    transaction_type: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    transaction_date: datetime
    class Config:
        orm_mode = True

class DepositBase(BaseModel):
    amount: float
    payment_method: str
    status: str

class DepositCreate(DepositBase):
    pass

class Deposit(DepositBase):
    id: int
    deposit_date: datetime
    class Config:
        orm_mode = True

# Schemas for search results and logging can be added as needed.
