from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define the base class for the ORM models
Base = declarative_base()

# Define the Users table
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

# Define the Categories table
class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=False, unique=True)

# Define the Expenses table
class Expense(Base):
    __tablename__ = 'expenses'
    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)

    user = relationship("User")
    category = relationship("Category")

# Define the Inventory table
class InventoryItem(Base):
    __tablename__ = 'inventory'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)

# Define the Sales table
class Sale(Base):
    __tablename__ = 'sales'
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    items_sold = Column(String)  # This can be a JSON string or a simple comma-separated list

    user = relationship("User")

# Define the SalesItems table
class SalesItem(Base):
    __tablename__ = 'sales_items'
    sale_item_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sales.sale_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('inventory.item_id'), nullable=False)
    quantity_sold = Column(Integer, nullable=False)

    sale = relationship("Sale")
    item = relationship("InventoryItem")

# Create a SQLite database
engine = create_engine('sqlite:///../database.db')

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()