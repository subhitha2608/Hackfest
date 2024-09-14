
import unittest
from your_module import calculate_credit_score  # import the function to be tested

class TestCalculateCreditScore(unittest.TestCase):
    def setUp(self):
        # create a test database connection (you can use a testing database)
        self.engine = create_engine('postgresql://user:password@localhost/test_database')

    def tearDown(self):
        # close the database connection
        self.engine.dispose()

    def test_calculate_credit_score_happy_path(self):
        # create test data
        customer_id = 1
        loan_data = [
            {'customer_id': customer_id, 'loan_amount': 1000, 'repayment_amount': 500, 'outstanding_balance': 500},
            {'customer_id': customer_id, 'loan_amount': 2000, 'repayment_amount': 1000, 'outstanding_balance': 1000},
        ]
        credit_card_data = [{'customer_id': customer_id, 'balance': 500}]
        payment_data = [{'customer_id': customer_id, 'status': 'On Time'}]
        self.engine.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)"), loan_data)
        self.engine.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)"), credit_card_data)
        self.engine.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, :status)"), payment_data)

        # call the function
        credit_score = calculate_credit_score(customer_id)

        # assert the result
        self.assertAlmostEqual(credit_score, 760, places=0)  # expected credit score based on the test data

    def test_calculate_credit_score_no_loans(self):
        customer_id = 2
        credit_card_data = [{'customer_id': customer_id, 'balance': 0}]
        payment_data = [{'customer_id': customer_id, 'status': 'On Time'}]
        self.engine.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)"), credit_card_data)
        self.engine.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, :status)"), payment_data)

        # call the function
        credit_score = calculate_credit_score(customer_id)

        # assert the result
        self.assertEqual(credit_score, 700)  # expected credit score when no loans

    def test_calculate_credit_score_no_credit_cards(self):
        customer_id = 3
        loan_data = [
            {'customer_id': customer_id, 'loan_amount': 1000, 'repayment_amount': 500, 'outstanding_balance': 500},
        ]
        payment_data = [{'customer_id': customer_id, 'status': 'On Time'}]
        self.engine.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)"), loan_data)
        self.engine.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, :status)"), payment_data)

        # call the function
        credit_score = calculate_credit_score(customer_id)

        # assert the result
        self.assertAlmostEqual(credit_score, 600, places=0)  # expected credit score when no credit cards

    def test_calculate_credit_score_late_payments(self):
        customer_id = 4
        loan_data = [
            {'customer_id': customer_id, 'loan_amount': 1000, 'repayment_amount': 500, 'outstanding_balance': 500},
        ]
        credit_card_data = [{'customer_id': customer_id, 'balance': 500}]
        payment_data = [{'customer_id': customer_id, 'status': 'Late'}]
        self.engine.execute(text("INSERT INTO loans (customer_id, loan_amount, repayment_amount, outstanding_balance) VALUES (:customer_id, :loan_amount, :repayment_amount, :outstanding_balance)"), loan_data)
        self.engine.execute(text("INSERT INTO credit_cards (customer_id, balance) VALUES (:customer_id, :balance)"), credit_card_data)
        self.engine.execute(text("INSERT INTO payments (customer_id, status) VALUES (:customer_id, :status)"), payment_data)

        # call the function
        credit_score = calculate_credit_score(customer_id)

        # assert the result
        self.assertAlmostEqual(credit_score, 500, places=0)  # expected credit score with late payments

    def test_calculate_credit_score_invalid_customer_id(self):
        customer_id = -1
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

    def test_calculate_credit_score_db_error(self):
        def mock_execute(query, **kwargs):
            raise psycopg2.Error(' db error ')
        self.engine.execute = mock_execute
        customer_id = 1
        with self.assertRaises(psycopg2.Error):
            calculate_credit_score(customer_id)

if __name__ == '__main__':
    unittest.main()
