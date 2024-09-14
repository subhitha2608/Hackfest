
import unittest
from your_module import calculate_credit_score  # import the function to be tested
import pandas as pd
from sqlalchemy import create_engine

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Set up a test database engine
        self.engine = create_engine('postgresql://user:password@host:port/dbname')
        self.conn = self.engine.connect()

    def tearDown(self):
        # Clean up the test database engine
        self.conn.close()

    def test_calculate_credit_score_positive(self):
        # Create test data
        customer_id = 1
        loan_amount = 1000
        repayment_amount = 500
        outstanding_balance = 500
        credit_card_balance = 2000
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)"), 
                           {"customer_id": customer_id, "loan_amount": loan_amount, "repayment_amount": repayment_amount, "outstanding_balance": outstanding_balance})
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)"), 
                           {"customer_id": customer_id, "balance": credit_card_balance})
        self.conn.commit()

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertIsInstance(credit_score, int)
        self.assertGreaterEqual(credit_score, 300)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_zero_loan_amount(self):
        # Create test data
        customer_id = 1
        loan_amount = 0
        repayment_amount = 0
        outstanding_balance = 0
        credit_card_balance = 2000
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)"), 
                           {"customer_id": customer_id, "loan_amount": loan_amount, "repayment_amount": repayment_amount, "outstanding_balance": outstanding_balance})
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)"), 
                           {"customer_id": customer_id, "balance": credit_card_balance})
        self.conn.commit()

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertIsInstance(credit_score, int)
        self.assertEqual(credit_score, 700)

    def test_calculate_credit_score_high_credit_card_balance(self):
        # Create test data
        customer_id = 1
        loan_amount = 1000
        repayment_amount = 500
        outstanding_balance = 500
        credit_card_balance = 8000
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)"), 
                           {"customer_id": customer_id, "loan_amount": loan_amount, "repayment_amount": repayment_amount, "outstanding_balance": outstanding_balance})
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)"), 
                           {"customer_id": customer_id, "balance": credit_card_balance})
        self.conn.commit()

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertIsInstance(credit_score, int)
        self.assertLessEqual(credit_score, 500)

    def test_calculate_credit_score_late_payments(self):
        # Create test data
        customer_id = 1
        loan_amount = 1000
        repayment_amount = 500
        outstanding_balance = 500
        credit_card_balance = 2000
        late_pay_count = 2

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)"), 
                           {"customer_id": customer_id, "loan_amount": loan_amount, "repayment_amount": repayment_amount, "outstanding_balance": outstanding_balance})
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)"), 
                           {"customer_id": customer_id, "balance": credit_card_balance})
        self.conn.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, 'Late')"), 
                         {"customer_id": customer_id})
        self.conn.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, 'Late')"), 
                         {"customer_id": customer_id})
        self.conn.commit()

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertIsInstance(credit_score, int)
        self.assertLessEqual(credit_score, 400)

    def test_calculate_credit_score_invalid_customer_id(self):
        # Create test data
        customer_id = 999  # invalid customer ID

        # Call the function to be tested
        with self.assertRaises(TypeError):
            calculate_credit_score(customer_id)

    def test_calculate_credit_score_no_data(self):
        # Create test data
        customer_id = 1

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertIsNone(credit_score)

if __name__ == '__main__':
    unittest.main()
