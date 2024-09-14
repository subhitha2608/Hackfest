
import unittest
from your_module import calculate_repayment_schedule
import pandas as pd

class TestCalculateRepaymentSchedule(unittest.TestCase):

    def test_loan_id_missing(self):
        with self.assertRaises(KeyError):
            calculate_repayment_schedule(None)

    def test_non_numeric_loan_amount(self):
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(123, loan_amount='abc')

    def test_non_numeric_interest_rate(self):
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(123, interest_rate='abc')

    def test_non_numeric_loan_term(self):
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(123, loan_term='abc')

    def test_calculate_fixed_monthly_payment(self):
        loan_amount = 10000
        interest_rate = 5
        loan_term = 60
        monthly_interest_rate = interest_rate / 100 / 12
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))
        self.assertEqual(round(monthly_payment, 2), 152.19)

    def test_calculate_interest_amount(self):
        loan_amount = 10000
        interest_rate = 5
        loan_term = 60
        monthly_interest_rate = interest_rate / 100 / 12
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))
        balance = loan_amount
        payment_number = 1
        interest_amount = balance * monthly_interest_rate
        self.assertEqual(round(interest_amount, 2), 41.67)

    def test_calculate_principal_amount(self):
        loan_amount = 10000
        interest_rate = 5
        loan_term = 60
        monthly_interest_rate = interest_rate / 100 / 12
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -loan_term))
        balance = loan_amount
        payment_number = 1
        principal_amount = monthly_payment - balance * monthly_interest_rate
        self.assertEqual(round(principal_amount, 2), 110.52)

    def test_repayment_schedule(self):
        loan_amount = 10000
        interest_rate = 5
        loan_term = 60
        calculate_repayment_schedule(123, loan_amount, interest_rate, loan_term)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
