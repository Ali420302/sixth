from dal import dal
from utils.security import check_password

# User Management
def register_user(username, password, email):
    try:
        dal.add_user(username, password, email)
    except ValueError as e:
        print(e)

def modify_user(user_id, username=None, password=None, email=None):
    try:
        dal.update_user(user_id, username, password, email)
    except ValueError as e:
        print(e)

def remove_user(user_id):
    dal.delete_user(user_id)

def list_users():
    return dal.get_all_users()

def authenticate_user(username, password):
    user = dal.get_user_by_username(username)
    if user and check_password(user.password, password):
        return user
    return None

def get_user_by_username(username):
    return dal.get_user_by_username(username)

def get_user_by_email(email):
    return dal.get_user_by_email(email)

# Expense Management
def record_expense(user_id, category_id, date, amount, description):
    dal.add_expense(user_id, category_id, date, amount, description)

def view_expense_history(user_id):
    return dal.get_expense_history(user_id)

# Inventory Management
def add_inventory(item_name, quantity, cost):
    dal.add_inventory_item(item_name, quantity, cost)

def update_inventory(item_id, item_name=None, quantity=None, cost=None):
    dal.update_inventory_item(item_id, item_name, quantity, cost)

def delete_inventory(item_id):
    dal.delete_inventory_item(item_id)

def list_inventory():
    return dal.get_all_inventory_items()

# Sales Management
def record_sale(user_id, date, amount, items_sold):
    dal.add_sale(user_id, date, amount, items_sold)

def view_sales_history(user_id):
    return dal.get_sales_history(user_id)

# Reporting
def generate_report():
    report = dal.generate_financial_report()
    return report
