import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, Expense, InventoryItem, Sale
from dal import dal

class TestGenerateFinancialReport(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Inject the session into the DAL
        dal.session = self.session

        # Add test data
        user1 = User(username='user1', email='user1@example.com', password='password1')
        user2 = User(username='user2', email='user2@example.com', password='password2')
        self.session.add_all([user1, user2])
        self.session.commit()

        expense1 = Expense(user_id=user1.user_id, category_id=1, date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(), amount=100.0, description='Test Expense 1')
        expense2 = Expense(user_id=user2.user_id, category_id=2, date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(), amount=200.0, description='Test Expense 2')
        self.session.add_all([expense1, expense2])
        self.session.commit()

        inventory_item1 = InventoryItem(item_name='Item1', quantity=10, cost=50.0)
        inventory_item2 = InventoryItem(item_name='Item2', quantity=20, cost=100.0)
        self.session.add_all([inventory_item1, inventory_item2])
        self.session.commit()

        sale1 = Sale(user_id=user1.user_id, date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(), amount=500.0, items_sold='Item1')
        sale2 = Sale(user_id=user2.user_id, date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(), amount=700.0, items_sold='Item2')
        self.session.add_all([sale1, sale2])
        self.session.commit()

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_generate_financial_report(self):
        report = dal.generate_financial_report()
        expected_report = {
            'total_expenses': 300.0,
            'total_inventory_value': 2500.0,
            'total_sales': 1200.0,
            'profit': 900.0
        }
        self.assertEqual(report, expected_report)

if __name__ == '__main__':
    unittest.main()