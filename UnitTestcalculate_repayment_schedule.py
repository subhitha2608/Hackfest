
import unittest
from your_module import calculate_repayment_schedule  # Import the function to be tested

class TestCalculateRepaymentSchedule(unittest.TestCase):
    def test_loan_id_1(self):
        calculate_repayment_schedule(1)
        conn = engine.connect()
        result = conn.execute("SELECT COUNT(*) FROM repaymentschedule WHERE loanid = 1")
        count = result.fetchone()[0]
        self.assertEqual(count, 12)  # Assuming a 1-year loan with 12 monthly payments
        conn.close()

    def test_loan_id_2(self):
        calculate_repayment_schedule(2)
        conn = engine.connect()
        result = conn.execute("SELECT SUM(principalamount) FROM repaymentschedule WHERE loanid = 2")
        total_principal = result.fetchone()[0]
        self.assertEqual(total_principal, 10000.0)  # Assuming a loan with total principal amount of 10000.0
        conn.close()

    def test_loan_id_non_existent(self):
        with self.assertRaises(psycopg2.Error):
            calculate_repayment_schedule(999)  # Assuming loan ID 999 does not exist in the database

if __name__ == '__main__':
    unittest.main()
