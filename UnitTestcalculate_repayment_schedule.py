
import unittest
from your_module import generate_repayment_schedule

class TestGenerateRepaymentSchedule(unittest.TestCase):
    def test_valid_loan_id(self):
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        selfassertIsNotNone(repayment_schedule)
        selfassertGreaterThan(len(repayment_schedule), 0)

    def test_invalid_loan_id(self):
        loan_id = -1
        with self.assertRaises(Exception):
            generate_repayment_schedule(loan_id)

    def test_loan_id_not_found(self):
        loan_id = 1000  # assume this loan ID does not exist in the database
        with self.assertRaises(Exception):
            generate_repayment_schedule(loan_id)

    def test_zero_loan_amount(self):
        loan_id = 1
        # assume the loan amount for this loan ID is 0
        with self.assertRaises(ZeroDivisionError):
            generate_repayment_schedule(loan_id)

    def test_negative_loan_amount(self):
        loan_id = 2
        # assume the loan amount for this loan ID is negative
        with self.assertRaises(ValueError):
            generate_repayment_schedule(loan_id)

    def test_invalid_interest_rate(self):
        loan_id = 3
        # assume the interest rate for this loan ID is invalid (e.g. negative or > 100)
        with self.assertRaises(ValueError):
            generate_repayment_schedule(loan_id)

    def test_loan_term_zero(self):
        loan_id = 4
        # assume the loan term for this loan ID is 0
        with self.assertRaises(ZeroDivisionError):
            generate_repayment_schedule(loan_id)

    def test_loan_term_negative(self):
        loan_id = 5
        # assume the loan term for this loan ID is negative
        with self.assertRaises(ValueError):
            generate_repayment_schedule(loan_id)

    def test_repayment_schedule_content(self):
        loan_id = 1
        repayment_schedule = generate_repayment_schedule(loan_id)
        selfassertIsNotNone(repayment_schedule)
        for detail in repayment_schedule:
            selfassertIn("loan_id", detail)
            selfassertIn("payment_number", detail)
            selfassertIn("payment_date", detail)
            selfassertIn("principal_amount", detail)
            selfassertIn("interest_amount", detail)
            selfassertIn("total_payment", detail)
            selfassertIn("balance", detail)

if __name__ == '__main__':
    unittest.main()
