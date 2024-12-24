from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models.models import User, Category, Expense, InventoryItem, Sale, SalesItem, engine
from utils.security import hash_password, check_password

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# User Management
def add_user(username, password, email):
    if get_user_by_username(username):
        raise ValueError("Username already exists")
    if get_user_by_email(email):
        raise ValueError("Email already exists")
    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password, email=email)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Failed to add user due to a database error")

def update_user(user_id, username=None, password=None, email=None):
    user = session.query(User).filter_by(user_id=user_id).first()
    if username:
        if get_user_by_username(username):
            raise ValueError("Username already exists")
        user.username = username
    if password:
        user.password = hash_password(password)
    if email:
        if get_user_by_email(email):
            raise ValueError("Email already exists")
        user.email = email
    session.commit()

def delete_user(user_id):
    user = session.query(User).filter_by(user_id=user_id).first()
    session.delete(user)
    session.commit()

def get_all_users():
    return session.query(User).all()

def get_user_by_username(username):
    return session.query(User).filter_by(username=username).first()

def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

# Expense Management
def add_expense(user_id, category_id, date, amount, description):
    expense = Expense(user_id=user_id, category_id=category_id, date=datetime.strptime(date, '%Y-%m-%d').date(), amount=amount, description=description)
    session.add(expense)
    session.commit()

def get_expense_history(user_id):
    return session.query(Expense).filter_by(user_id=user_id).all()

# Inventory Management
def add_inventory_item(item_name, quantity, cost):
    item = InventoryItem(item_name=item_name, quantity=quantity, cost=cost)
    session.add(item)
    session.commit()

def update_inventory_item(item_id, item_name=None, quantity=None, cost=None):
    item = session.query(InventoryItem).filter_by(item_id=item_id).first()
    if item_name:
        item.item_name = item_name
    if quantity:
        item.quantity = quantity
    if cost:
        item.cost = cost
    session.commit()

def delete_inventory_item(item_id):
    item = session.query(InventoryItem).filter_by(item_id=item_id).first()
    session.delete(item)
    session.commit()

def get_all_inventory_items():
    return session.query(InventoryItem).all()

# Sales Management
def add_sale(user_id, date, amount, items_sold):
    sale = Sale(user_id=user_id, date=datetime.strptime(date, '%Y-%m-%d').date(), amount=amount, items_sold=items_sold)
    session.add(sale)
    session.commit()

def get_sales_history(user_id):
    return session.query(Sale).filter_by(user_id=user_id).all()

def generate_financial_report():
    # Fetch expenses, inventory, and sales data
    expenses = session.query(Expense).all()
    inventory = session.query(InventoryItem).all()
    sales = session.query(Sale).all()

    # Generate a simple report
    report = {
        'total_expenses': sum(expense.amount for expense in expenses),
        'total_inventory_value': sum(item.cost * item.quantity for item in inventory),
        'total_sales': sum(sale.amount for sale in sales),
        'profit': sum(sale.amount for sale in sales) - sum(expense.amount for expense in expenses)
    }

    return report