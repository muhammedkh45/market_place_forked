from sqlalchemy.orm import Session
from app import models, schemas

# Example CRUD functions for Users

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def create_user(db: Session, user: schemas.UserCreate):
    account_data = create_account(db, user.account)
    db_user = models.User(balance=user.balance, account_id=account_data.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Other CRUD functions for items, transactions, etc., can be added similarly.
def get_items_by_query(db: Session, query: str):
    return db.query(models.Item).filter(models.Item.name.ilike(f"%{query}%")).all()