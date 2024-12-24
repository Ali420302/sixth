import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, Expense, InventoryItem, Sale
from utils.security import hash_password

class TestModels(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_user_model(self):
        # Create and add a new user
        user = User(username='testuser', email='testuser@example.com', password=hash_password('password'))
        self.session.add(user)
        self.session.commit()

        # Retrieve the user
        retrieved_user = self.session.query(User).filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'testuser@example.com')

        # Update the user's email
        retrieved_user.email = 'newemail@example.com'
        self.session.commit()
        updated_user = self.session.query(User).filter_by(username='testuser').first()
        self.assertEqual(updated_user.email, 'newemail@example.com')

        # Delete the user
        self.session.delete(updated_user)
        self.session.commit()
        deleted_user = self.session.query(User).filter_by(username='testuser').first()
        self.assertIsNone(deleted_user)

    def test_expense_model(self):
        # Create and add a new expense
        expense = Expense(user_id=1, category_id=1, date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(), amount=100.0, description='Test Expense')
        self.session.add(expense)
        self.session.commit()

        # Retrieve the expense
        retrieved_expense = self.session.query(Expense).filter_by(description='Test Expense').first()
        self.assertIsNotNone(retrieved_expense)
        self.assertEqual(retrieved_expense.amount, 100.0)

        # Update the expense amount
        retrieved_expense.amount = 200.0
        self.session.commit()
        updated_expense = self.session.query(Expense).filter_by(description='Test Expense').first()
        self.assertEqual(updated_expense.amount, 200.0)

        # Delete the expense
        self.session.delete(updated_expense)
        self.session.commit()
        deleted_expense = self.session.query(Expense).filter_by(description='Test Expense').first()
        self.assertIsNone(deleted_expense)

    def test_inventory_model(self):
        # Create and add a new inventory item
        inventory_item = InventoryItem(item_name='Test Item', quantity=10, cost=50.0)
        self.session.add(inventory_item)
        self.session.commit()

        # Retrieve the inventory item
        retrieved_item = self.session.query(InventoryItem).filter_by(item_name='Test Item').first()
        self.assertIsNotNone(retrieved_item)
        self.assertEqual(retrieved_item.quantity, 10)

        # Update the inventory item quantity
        retrieved_item.quantity = 20
        self.session.commit()
        updated_item = self.session.query(InventoryItem).filter_by(item_name='Test Item').first()
        self.assertEqual(updated_item.quantity, 20)

        # Delete the inventory item
        self.session.delete(updated_item)
        self.session.commit()
        deleted_item = self.session.query(InventoryItem).filter_by(item_name='Test Item').first()
        self.assertIsNone(deleted_item)

    def test_sale_model(self):
        # Create and add a new sale
        sale = Sale(user_id=1, date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(), amount=500.0, items_sold='Test Item')
        self.session.add(sale)
        self.session.commit()

        # Retrieve the sale
        retrieved_sale = self.session.query(Sale).filter_by(items_sold='Test Item').first()
        self.assertIsNotNone(retrieved_sale)
        self.assertEqual(retrieved_sale.amount, 500.0)

        # Update the sale amount
        retrieved_sale.amount = 600.0
        self.session.commit()
        updated_sale = self.session.query(Sale).filter_by(items_sold='Test Item').first()
        self.assertEqual(updated_sale.amount, 600.0)

        # Delete the sale
        self.session.delete(updated_sale)
        self.session.commit()
        deleted_sale = self.session.query(Sale).filter_by(items_sold='Test Item').first()
        self.assertIsNone(deleted_sale)

if __name__ == '__main__':
    unittest.main()