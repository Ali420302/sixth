import sys
import bll.bll as bll
from utils.validation import is_valid_email

current_user = None


def main_menu():
    print("Welcome to Brew and Bite Café Expense Tracking System")
    print("1. Login")
    print("2. Signup")
    print("3. Exit")


def user_menu():
    print("User Menu")
    print("1. User Account Management")
    print("2. Expense Management")
    print("3. Inventory Management")
    print("4. Sales Management")
    print("5. Generate Report")
    print("6. Logout")


def user_account_management_menu():
    print("User Account Management")
    print("1. Update Account")
    print("2. View Account")
    print("3. Delete Account")
    print("4. Back to Main Menu")


def expense_management_menu():
    print("Expense Management")
    print("1. Record Expense")
    print("2. View Expense History")
    print("3. Back to Main Menu")


def inventory_management_menu():
    print("Inventory Management")
    print("1. Add Inventory Item")
    print("2. Update Inventory Item")
    print("3. Delete Inventory Item")
    print("4. List Inventory Items")
    print("5. Back to Main Menu")


def sales_management_menu():
    print("Sales Management")
    print("1. Record Sale")
    print("2. View Sales History")
    print("3. Back to Main Menu")


def generate_report_menu():
    print("Generate Report")
    print("1. Generate Financial Report")
    print("2. Back to Main Menu")


def main():
    global current_user
    while True:
        if current_user is None:
            main_menu()
            choice = input("Select an option: ")

            if choice == '1':
                login()
            elif choice == '2':
                signup()
            elif choice == '3':
                sys.exit()
            else:
                print("Invalid choice, please try again.")
        else:
            user_menu()
            choice = input("Select an option: ")

            if choice == '1':
                user_account_management()
            elif choice == '2':
                expense_management()
            elif choice == '3':
                inventory_management()
            elif choice == '4':
                sales_management()
            elif choice == '5':
                generate_report()
            elif choice == '6':
                current_user = None
            else:
                print("Invalid choice, please try again.")


def login():
    global current_user
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = bll.authenticate_user(username, password)
    if user:
        current_user = user
        print("Login successful.")
    else:
        print("Invalid username or password.")


def signup():
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        while True:
            email = input("Enter email: ")
            if not is_valid_email(email):
                print("Invalid email format. Please enter a valid email address.")
            else:
                break

        if bll.get_user_by_username(username):
            print("Username already exists. Please try with a different username.")
            continue

        if bll.get_user_by_email(email):
            print("Email already exists. Please try with a different email.")
            continue

        try:
            bll.register_user(username, password, email)
            print("User registered successfully.")
            break  # Exit the loop after successful registration
        except ValueError as e:
            print(e)
            print("Please try signing up again.")


def user_account_management():
    while True:
        user_account_management_menu()
        choice = input("Select an option: ")

        if choice == '1':
            update_account()
        elif choice == '2':
            view_account()
        elif choice == '3':
            delete_account()
        elif choice == '4':
            return
        else:
            print("Invalid choice, please try again.")


def update_account():
    global current_user
    user_id = current_user.user_id
    username = input("Enter new username (leave blank to keep current): ")
    password = input("Enter new password (leave blank to keep current): ")
    email = input("Enter new email (leave blank to keep current): ")

    if email and not is_valid_email(email):
        print("Invalid email format. Please enter a valid email address.")
        return

    try:
        bll.modify_user(user_id, username, password, email)
        if username:
            current_user.username = username
        if email:
            current_user.email = email
        print("Account updated successfully.")
    except ValueError as e:
        print(e)


def view_account():
    global current_user
    print(f"Username: {current_user.username}")
    print(f"Email: {current_user.email}")


def delete_account():
    global current_user
    confirmation = input("Are you sure you want to delete your account? This action cannot be undone. (yes/no): ")
    if confirmation.lower() == 'yes':
        bll.remove_user(current_user.user_id)
        current_user = None
        print("Account deleted successfully.")
    else:
        print("Account deletion cancelled.")


def expense_management():
    while True:
        expense_management_menu()
        choice = input("Select an option: ")

        if choice == '1':
            user_id = current_user.user_id
            category_id = int(input("Enter category ID: "))
            date = input("Enter date (YYYY-MM-DD): ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            bll.record_expense(user_id, category_id, date, amount, description)
            print("Expense recorded successfully.")
        elif choice == '2':
            user_id = current_user.user_id
            expenses = bll.view_expense_history(user_id)
            for expense in expenses:
                print(
                    f"Date: {expense.date}, Amount: {expense.amount}, Category ID: {expense.category_id}, Description: {expense.description}")
        elif choice == '3':
            return
        else:
            print("Invalid choice, please try again.")


def inventory_management():
    while True:
        inventory_management_menu()
        choice = input("Select an option: ")

        if choice == '1':
            item_name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            cost = float(input("Enter cost: "))
            bll.add_inventory(item_name, quantity, cost)
            print("Inventory item added successfully.")
        elif choice == '2':
            item_id = int(input("Enter item ID: "))
            item_name = input("Enter new item name (leave blank to keep current): ")
            quantity = input("Enter new quantity (leave blank to keep current): ")
            cost = input("Enter new cost (leave blank to keep current): ")
            bll.update_inventory(item_id, item_name, quantity, cost)
            print("Inventory item updated successfully.")
        elif choice == '3':
            item_id = int(input("Enter item ID: "))
            bll.delete_inventory(item_id)
            print("Inventory item deleted successfully.")
        elif choice == '4':
            items = bll.list_inventory()
            for item in items:
                print(f"ID: {item.item_id}, Name: {item.item_name}, Quantity: {item.quantity}, Cost: {item.cost}")
        elif choice == '5':
            return
        else:
            print("Invalid choice, please try again.")


def sales_management():
    while True:
        sales_management_menu()
        choice = input("Select an option: ")

        if choice == '1':
            user_id = current_user.user_id
            date = input("Enter date (YYYY-MM-DD): ")
            amount = float(input("Enter amount: "))
            items_sold = input("Enter items sold (comma-separated): ")
            bll.record_sale(user_id, date, amount, items_sold)
            print("Sale recorded successfully.")
        elif choice == '2':
            user_id = current_user.user_id
            sales = bll.view_sales_history(user_id)
            for sale in sales:
                print(f"Date: {sale.date}, Amount: {sale.amount}, Items Sold: {sale.items_sold}")
        elif choice == '3':
            return
        else:
            print("Invalid choice, please try again.")


def generate_report():
    while True:
        generate_report_menu()
        choice = input("Select an option: ")

        if choice == '1':
            report = bll.generate_report()
            if report:
                print("Financial Report:")
                print(f"Total Expenses: {report['total_expenses']}")
                print(f"Total Inventory Value: {report['total_inventory_value']}")
                print(f"Total Sales: {report['total_sales']}")
                print(f"Profit: {report['profit']}")
            else:
                print("No data available to generate the report.")
        elif choice == '2':
            return
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()