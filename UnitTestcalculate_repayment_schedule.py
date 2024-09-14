
import unittest
from your_module import calculate_repayment_schedule
import datetime

class TestCalculateRepaymentSchedule(unittest.TestCase):

    def test_valid_loan(self):
        loan_id = 1
        loan_amount = 100000
        interest_rate = 6
        loan_term = 60

        # Mock the engine and connection
        engine = MockEngine()
        engine.execute.return_value = [(loan_amount, interest_rate, loan_term, datetime.date(2022, 1, 1))]

        # Call the function
        data = calculate_repayment_schedule(loan_id)

        # Check the length of the data
        self.assertEqual(len(data), loan_term)

        # Check the values in the data
        for i, row in enumerate(data):
            payment_date = datetime.date(2022, 1, 1) + datetime.timedelta(days=30*(i+1))
            expected_principal_amount = (loan_amount - loan_amount * (1 + interest_rate/100/12)**(-i-1)) - (loan_amount - loan_amount * (1 + interest_rate/100/12)**(-i-2))
            expected_interest_amount = loan_amount * (1 + interest_rate/100/12)**(-i-1) - (loan_amount - loan_amount * (1 + interest_rate/100/12)**(-i-2))
            expected_monthly_payment = (loan_amount * interest_rate/100/12) / (1 - (1 + interest_rate/100/12)**(-loan_term))
            self.assertEqual(row["payment_date"], payment_date)
            self.assertAlmostEqual(row["principal_amount"], expected_principal_amount, places=6)
            self.assertAlmostEqual(row["interest_amount"], expected_interest_amount, places=6)
            self.assertAlmostEqual(row["totalpayment"], expected_monthly_payment, places=6)

    def test_invalid_loan_id(self):
        loan_id = 0
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(loan_id)

    def test_loans_table_empty(self):
        engine = MockEngine()
        engine.execute.return_value = None
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(1)

    def test_connection_error(self):
        engine = MockEngine()
        engine.execute.side_effect = psycopg2.Error(' mock error')
        with self.assertRaises(psycopg2.Error):
            calculate_repayment_schedule(1)

class MockEngine:
    def __init__(self):
        self.execute = lambda query, params: MockConnection(query, params)

class MockConnection:
    def __init__(self, query, params):
        self.query = query
        self.params = params

    def fetchone(self):
        return [(100000, 6, 60, datetime.date(2022, 1, 1))]

if __name__ == '__main__':
    unittest.main()
