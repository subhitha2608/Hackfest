
import unittest
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    def test_repayment_schedule(self):
        loan_id = 1
        calculate_repayment_schedule(loan_id)

    def test_loan_id_type(self):
        with self.assertRaises(TypeError):
            calculate_repayment_schedule('abc')

    def test_loan_id_non_integer(self):
        with self.assertRaises(TypeError):
            calculate_repayment_schedule(3.14)

    def test_loan_details_empty(self):
        loan_id = 100
        with self.assertRaises(Exception):
            calculate_repayment_schedule(loan_id)

    def test_loan_term_zero(self):
        loan_id = 1
        with self.assertRaises Exception:
            calculate_repayment_schedule(loan_id)

    def test_monthly_payment_division_by_zero(self):
        loan_id = 1
        interest_rate = 0
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(loan_id, interest_rate=interest_rate)

    def test_payment_date_type(self):
        loan_id = 1
        with self.assertRaises(TypeError):
            payment_date = '2020-01-01'
            calculate_repayment_schedule(loan_id, payment_date = payment_date)

    def test_repayment_schedule_insertion(self):
        loan_id = 1
        conn = engine.connect()
        query = text("""
            SELECT * FROM repaymentschedule
            WHERE loanid = :loan_id
        """)
        initial_rows = conn.execute(query, loan_id=loan_id).fetchall()
        conn.close()
        calculate_repayment_schedule(loan_id)
        query = text("""
            SELECT * FROM repaymentschedule
            WHERE loanid = :loan_id
        """)
        new_rows = conn.execute(query, loan_id=loan_id).fetchall()
        conn.close()
        self.assertTrue(initial_rows != new_rows)

if __name__ == '__main__':
    unittest.main()
