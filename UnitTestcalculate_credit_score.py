
import unittest
from your_module import calculate_credit_score  # Import the function to be tested

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Create a test database connection or engine
        self.engine = create_engine('postgresql://user:password@host:port/dbname')

    def tearDown(self):
        # Close the database connection or engine
        self.engine.dispose()

    def test_calculate_credit_score_positive(self):
        # Test with positive data
        customer_id = 1
        total_loan_amount = 10000.0
        total_repayment = 8000.0
        outstanding_loan_balance = 2000.0
        credit_card_balance = 500.0
        late_pay_count = 0

        # Insert test data into the database
        self.engine.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)" % (customer_id, total_loan_amount, total_repayment, outstanding_loan_balance))
        self.engine.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)" % (customer_id, credit_card_balance))
        self.engine.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'On Time')" % customer_id)

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertGreaterEqual(credit_score, 700)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_negative(self):
        # Test with negative data
        customer_id = 2
        total_loan_amount = 0.0
        total_repayment = 0.0
        outstanding_loan_balance = 0.0
        credit_card_balance = 0.0
        late_pay_count = 5

        # Insert test data into the database
        self.engine.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)" % (customer_id, total_loan_amount, total_repayment, outstanding_loan_balance))
        self.engine.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)" % (customer_id, credit_card_balance))
        self.engine.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')" % customer_id)
        self.engine.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')" % customer_id)
        self.engine.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')" % customer_id)
        self.engine.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')" % customer_id)
        self.engine.execute("INSERT INTO payments (customer_id, status) VALUES (%s, 'Late')" % customer_id)

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertLessEqual(credit_score, 500)

    def test_calculate_credit_score_zero_loan_amount(self):
        # Test with zero loan amount
        customer_id = 3
        total_loan_amount = 0.0
        total_repayment = 0.0
        outstanding_loan_balance = 0.0
        credit_card_balance = 0.0
        late_pay_count = 0

        # Insert test data into the database
        self.engine.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)" % (customer_id, total_loan_amount, total_repayment, outstanding_loan_balance))
        self.engine.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)" % (customer_id, credit_card_balance))

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertEqual(credit_score, 700)

    def test_calculate_credit_score_zero_credit_card_balance(self):
        # Test with zero credit card balance
        customer_id = 4
        total_loan_amount = 10000.0
        total_repayment = 8000.0
        outstanding_loan_balance = 2000.0
        credit_card_balance = 0.0
        late_pay_count = 0

        # Insert test data into the database
        self.engine.execute("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (%s, %s, %s, %s)" % (customer_id, total_loan_amount, total_repayment, outstanding_loan_balance))
        self.engine.execute("INSERT INTO credit_cards (customer_id, balance) VALUES (%s, %s)" % (customer_id, credit_card_balance))

        # Call the function to be tested
        credit_score = calculate_credit_score(customer_id)

        # Assert the result
        self.assertGreaterEqual(credit_score, 700)
        self.assertLessEqual(credit_score, 850)

    def test_calculate_credit_score_nonexistent_customer(self):
        # Test with nonexistent customer
        customer_id = 999

        # Call the function to be tested
        with self.assertRaises(Exception):
            calculate_credit_score(customer_id)

if __name__ == '__main__':
    unittest.main()
