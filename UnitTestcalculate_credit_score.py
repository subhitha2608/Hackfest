
import unittest
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = engine.connect()

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_calculate_credit_score_all_positive(self):
        # Create test data
        customer_id = 1
        loan_amounts = [(1000, 500, 0), (2000, 1000, 0)]  # total loan amount, total repayment, outstanding balance
        credit_card_balance = 5000
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)", {"customer_id": customer_id, "loan_amount": loan_amounts[0][0], "repayment_amount": loan_amounts[0][1], "outstanding_balance": loan_amounts[0][2]}))
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)", {"customer_id": customer_id, "loan_amount": loan_amounts[1][0], "repayment_amount": loan_amounts[1][1], "outstanding_balance": loan_amounts[1][2]}))
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)", {"customer_id": customer_id, "balance": credit_card_balance}))
        self.conn.commit()

        # Call the function
        credit_score = calculate_credit_score(customer_id)

        # Assert that the credit score is calculated correctly
        self.assertAlmostEqual(credit_score, 740, places=0)

        # Clean up test data
        self.conn.execute(text("DELETE FROM loans WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.execute(text("DELETE FROM credit_cards WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.commit()

    def test_calculate_credit_score_all_zero(self):
        # Create test data
        customer_id = 2
        loan_amounts = [(0, 0, 0), (0, 0, 0)]  # total loan amount, total repayment, outstanding balance
        credit_card_balance = 0
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)", {"customer_id": customer_id, "loan_amount": loan_amounts[0][0], "repayment_amount": loan_amounts[0][1], "outstanding_balance": loan_amounts[0][2]}))
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)", {"customer_id": customer_id, "loan_amount": loan_amounts[1][0], "repayment_amount": loan_amounts[1][1], "outstanding_balance": loan_amounts[1][2]}))
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)", {"customer_id": customer_id, "balance": credit_card_balance}))
        self.conn.commit()

        # Call the function
        credit_score = calculate_credit_score(customer_id)

        # Assert that the credit score is calculated correctly
        self.assertEqual(credit_score, 700)

        # Clean up test data
        self.conn.execute(text("DELETE FROM loans WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.execute(text("DELETE FROM credit_cards WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.commit()

    def test_calculate_credit_score_no_loan_data(self):
        # Create test data
        customer_id = 3
        credit_card_balance = 5000
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)", {"customer_id": customer_id, "balance": credit_card_balance}))
        self.conn.commit()

        # Call the function
        credit_score = calculate_credit_score(customer_id)

        # Assert that the credit score is calculated correctly
        self.assertAlmostEqual(credit_score, 600, places=0)

        # Clean up test data
        self.conn.execute(text("DELETE FROM credit_cards WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.commit()

    def test_calculate_credit_score_no_credit_card_data(self):
        # Create test data
        customer_id = 4
        loan_amounts = [(1000, 500, 0), (2000, 1000, 0)]  # total loan amount, total repayment, outstanding balance
        late_pay_count = 0

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)", {"customer_id": customer_id, "loan_amount": loan_amounts[0][0], "repayment_amount": loan_amounts[0][1], "outstanding_balance": loan_amounts[0][2]}))
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)", {"customer_id": customer_id, "loan_amount": loan_amounts[1][0], "repayment_amount": loan_amounts[1][1], "outstanding_balance": loan_amounts[1][2]}))
        self.conn.commit()

        # Call the function
        credit_score = calculate_credit_score(customer_id)

        # Assert that the credit score is calculated correctly
        self.assertAlmostEqual(credit_score, 740, places=0)

        # Clean up test data
        self.conn.execute(text("DELETE FROM loans WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.commit()

    def test_calculate_credit_score_late_payments(self):
        # Create test data
        customer_id = 5
        loan_amounts = [(1000, 500, 0), (2000, 1000, 0)]  # total loan amount, total repayment, outstanding balance
        credit_card_balance = 5000
        late_pay_count = 2

        # Insert test data into the database
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)", {"customer_id": customer_id, "loan_amount": loan_amounts[0][0], "repayment_amount": loan_amounts[0][1], "outstanding_balance": loan_amounts[0][2]}))
        self.conn.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)", {"customer_id": customer_id, "loan_amount": loan_amounts[1][0], "repayment_amount": loan_amounts[1][1], "outstanding_balance": loan_amounts[1][2]}))
        self.conn.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)", {"customer_id": customer_id, "balance": credit_card_balance}))
        self.conn.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, 'Late')"), {"customer_id": customer_id})
        self.conn.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, 'Late')"), {"customer_id": customer_id})
        self.conn.commit()

        # Call the function
        credit_score = calculate_credit_score(customer_id)

        # Assert that the credit score is calculated correctly
        self.assertAlmostEqual(credit_score, 640, places=0)

        # Clean up test data
        self.conn.execute(text("DELETE FROM loans WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.execute(text("DELETE FROM credit_cards WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.execute(text("DELETE FROM payments WHERE customer_id = :customer_id", {"customer_id": customer_id}))
        self.conn.commit()

    def test_calculate_credit_score_invalid_customer_id(self):
        # Create test data
        customer_id = 999  # Non-existent customer ID

        # Call the function
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

if __name__ == '__main__':
    unittest.main()
