
import unittest
from unittest.mock import patch
from your_module import calculate_credit_score  # replace 'your_module' with the actual name of your module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)  # in-memory SQLite database
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Create some test data
        self.customer_id = 1
        self.total_loan_amount = 10000.0
        self.total_repayment = 5000.0
        self.outstanding_balance = 2000.0
        self.credit_card_balance = 1500.0
        self.late_pay_count = 2

        # Add test data to database
        self.session.execute('''
            INSERT INTO customers (id) VALUES (:customer_id)
        ''', {'customer_id': self.customer_id})
        self.session.execute('''
            INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :total_loan_amount, :total_repayment, :outstanding_balance)
        ''', {'customer_id': self.customer_id, 'total_loan_amount': self.total_loan_amount, 'total_repayment': self.total_repayment, 'outstanding_balance': self.outstanding_balance})
        self.session.execute('''
            INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :credit_card_balance)
        ''', {'customer_id': self.customer_id, 'credit_card_balance': self.credit_card_balance})
        self.session.execute('''
            INSERT INTO payments (customer_id, late_payment_count) VALUES (:customer_id, :late_pay_count)
        ''', {'customer_id': self.customer_id, 'late_pay_count': self.late_pay_count})

    def test_calculate_credit_score(self):
        with patch('your_module.engine', return_value=self.engine) as engine_mock:  # replace 'your_module' with the actual name of your module
            result = calculate_credit_score(self.customer_id)
            self.assertEqual(result, 550)  # expected credit score based on test data

    def test_calculate_credit_score_with_zero_total_loan_amount(self):
        with patch('your_module.engine', return_value=self.engine):
            self.session.execute('''
                UPDATE loans SET loan_amount = 0 WHERE customer_id = :customer_id
            ''', {'customer_id': self.customer_id})
            result = calculate_credit_score(self.customer_id)
            self.assertEqual(result, 400)

    def test_calculate_credit_score_with_zero_credit_card_balance(self):
        with patch('your_module.engine', return_value=self.engine):
            self.session.execute('''
                UPDATE credit_cards SET balance = 0 WHERE customer_id = :customer_id
            ''', {'customer_id': self.customer_id})
            result = calculate_credit_score(self.customer_id)
            self.assertEqual(result, 530)

    def test_calculate_credit_score_with_zero_late_pay_count(self):
        with patch('your_module.engine', return_value=self.engine):
            self.session.execute('''
                UPDATE payments SET late_payment_count = 0 WHERE customer_id = :customer_id
            ''', {'customer_id': self.customer_id})
            result = calculate_credit_score(self.customer_id)
            self.assertEqual(result, 630)

    def test_calculate_credit_score_with_update_failure(self):
        with patch('your_module.engine', return_value=self.engine) as engine_mock:
            with patch('your_module.engine.execute') as execute_mock:
                execute_mock.side_effect = Exception('Update failed')
                with self.assertRaises(Exception):
                    calculate_credit_score(self.customer_id)
                execute_mock.assert_called_once_with(text("""
                    UPDATE customers
                    SET credit_score = ROUND(:v_credit_score, 0)
                    WHERE customers.id = :customer_id
                """), {"customer_id": self.customer_id, "v_credit_score": 550})

    def tearDown(self):
        self.session.rollback()
        self.session.close()

if __name__ == '__main__':
    unittest.main()
