from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

# Account & User models
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)
    is_active = Column(Boolean, default=True)
    
    # One-to-one relationship with User
    user = relationship("User", back_populates="account", uselist=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    
    account = relationship("Account", back_populates="user")
    # One-to-many: User has many transactions and deposits
    transactions = relationship("Transaction", back_populates="user")
    deposits = relationship("Deposit", back_populates="user")
    # One-to-one: User has one InventoryPartition
    inventory_partition = relationship("InventoryPartition", back_populates="user", uselist=False)

# Inventory is a singleton: we'll simulate that in our app logic.
class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    # Relationship: one inventory has many partitions
    partitions = relationship("InventoryPartition", back_populates="inventory")

class InventoryPartition(Base):
    __tablename__ = "inventory_partitions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    
    user = relationship("User", back_populates="inventory_partition")
    inventory = relationship("Inventory", back_populates="partitions")
    # One-to-many: partition has many items
    items = relationship("Item", back_populates="partition")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    listed_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    partition_id = Column(Integer, ForeignKey("inventory_partitions.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    partition = relationship("InventoryPartition", back_populates="items")
    category = relationship("Category", back_populates="items")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    
    items = relationship("Item", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String)
    payment_method = Column(String)
    transaction_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="transactions")

class Deposit(Base):
    __tablename__ = "deposits"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    payment_method = Column(String)
    deposit_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="deposits")

# External System model
class ExternalSystem(Base):
    __tablename__ = "external_systems"
    id = Column(Integer, primary_key=True, index=True)
    system_name = Column(String)
    api_key = Column(String)
    auth_key = Column(String)
    integration_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
