
import unittest
import pandas as pd
from your_module import calculate_repayment_schedule  # Replace with the actual module name

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def setUp(self):
        # Create a test database connection
        self.conn = psycopg2.connect(
            host="localhost",
            database="test_db",
            user="test_user",
            password="test_password"
        )
        self.engine = create_engine("postgresql://test_user:test_password@localhost/test_db")

    def tearDown(self):
        # Close the test database connection
        self.conn.close()

    def test_calculate_repayment_schedule_valid_loan_id(self):
        # Insert a test loan record into the loans table
        loan_id = 1
        self.engine.execute(text("INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate) VALUES (:loan_id, 10000, 6, 36, '2022-01-01')"), {"loan_id": loan_id})

        # Call the function to calculate the repayment schedule
        repayment_schedule = calculate_repayment_schedule(loan_id)

        # Assert that the repayment schedule is returned as a pandas DataFrame
        self.assertIsInstance(repayment_schedule, pd.DataFrame)

        # Assert that the repayment schedule has the expected columns
        expected_columns = ['paymentnumber', 'paymentdate', 'principalamount', 'interestamount', 'totalpayment', 'balance']
        self.assertEqual(set(repayment_schedule.columns), set(expected_columns))

        # Assert that the repayment schedule has the expected number of rows
        self.assertEqual(len(repayment_schedule), 36)  # 36 months for a 36-month loan term

    def test_calculate_repayment_schedule_invalid_loan_id(self):
        # Call the function to calculate the repayment schedule with an invalid loan ID
        loan_id = 999  # Does not exist in the loans table
        with self.assertRaises(psycopg2.Error):
            calculate_repayment_schedule(loan_id)

    def test_calculate_repayment_schedule_no_loan_details_found(self):
        # Insert a test loan record into the loans table with missing details
        loan_id = 2
        self.engine.execute(text("INSERT INTO loans (loanid) VALUES (:loan_id)"), {"loan_id": loan_id})

        # Call the function to calculate the repayment schedule
        with self.assertRaises(AttributeError):
            calculate_repayment_schedule(loan_id)

    def test_calculate_repayment_scheduleLoanTerm(self):
        # Insert a test loan record into the loans table with a loan term of 0
        loan_id = 3
        self.engine.execute(text("INSERT INTO loans (loanid, loanamount, interestrate, loanterm, startdate) VALUES (:loan_id, 10000, 6, 0, '2022-01-01')"), {"loan_id": loan_id})

        # Call the function to calculate the repayment schedule
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(loan_id)

if __name__ == '__main__':
    unittest.main()
