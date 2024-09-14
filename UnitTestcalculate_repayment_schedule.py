Python
import unittest
from calculate_repayment import calculate_loan_repayment
import pandas as pd

class TestCalculateRepayment(unittest.TestCase):

    def test_calculate_loan_repayment(self):
        calculate_loan_repayment(1)

    def test_non_integer_loan_id(self):
        with self.assertRaises(TypeError):
            calculate_loan_repayment('one')

    def test_nonexistent_loan_id(self):
        with self.assertRaises(ValueError):
            calculate_loan_repayment(1000)

    def test_loan_with_zero_interest_rate(self):
        with self.assertRaises(ValueError):
            calculate_loan_repayment(1)

    def test_loan_with_zero_loan_term(self):
        with self.assertRaises(ValueError):
            calculate_loan_repayment(1)

    def test_loan_with_zero_loan_amount(self):
        with self.assertRaises(ValueError):
            calculate_loan_repayment(1)

    def test_loan_with_negative_loan_term(self):
        with self.assertRaises(ValueError):
            calculate_loan_repayment(1)

    def test_loan_with_negative_loan_amount(self):
        with self.assertRaises(ValueError):
            calculate_loan_repayment(1)

    def test_loan_with_negative_interest_rate(self):
        with self.assertRaises(ValueError):
            calculate_loan_repayment(1)

if __name__ == '__main__':
    unittest.main()
