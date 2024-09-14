
import unittest
from unittest.mock import patch, MagicMock
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine')
    def test_loan_id_not_found(self, mock_engine):
        mock_engine.execute.return_value.fetchone.return_value = None
        with self.assertRaises(ValueError):
            calculate_repayment_schedule(1)

    @patch('your_module.engine')
    def test_valid_loan_details(self, mock_engine):
        mock_engine.execute.return_value.fetchone.return_value = (1000, 5, 12, '2022-01-01')
        mock_engine.execute.return_value.lastrowid = 1
        calculate_repayment_schedule(1)
        mock_engine.execute.assert_called_with(
            sa.text("""
                INSERT INTO repaymentschedule (loanid, paymentnumber, paymentdate, principalamount, interestamount, totalpayment, balance)
                VALUES (:loan_id, :payment_number, :payment_date, :principal_amount, :interest_amount, :monthly_payment, :balance)
            """),
            {
                'loan_id': 1,
                'payment_number': 1,
                'payment_date': '2022-01-01',
                'principal_amount': 83.33,
                'interest_amount': 4.17,
                'monthly_payment': 87.50,
                'balance': 916.67
            }
        )

    @patch('your_module.engine')
    def test_zero_interest_rate(self, mock_engine):
        mock_engine.execute.return_value.fetchone.return_value = (1000, 0, 12, '2022-01-01')
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(1)

    @patch('your_module.engine')
    def test_zero_loan_term(self, mock_engine):
        mock_engine.execute.return_value.fetchone.return_value = (1000, 5, 0, '2022-01-01')
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(1)

    @patch('your_module.engine')
    def test_invalid_loan_id(self, mock_engine):
        with self.assertRaises(TypeError):
            calculate_repayment_schedule('invalid')

if __name__ == '__main__':
    unittest.main()
