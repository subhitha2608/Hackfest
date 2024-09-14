
import unittest
from unittest.mock import patch
from your_module import calculate_repayment_schedule

class TestCalculateRepaymentSchedule(unittest.TestCase):

    @patch('your_module.engine.connect')
    def test_loan_found(self, mock_connect):
        mock_connect.return_value.execute.return_value.fetchall.return_value = (
            (1000, 5, 60, '2022-01-01'),
        )
        mock_connect.return_value.close.return_value = None

        loan_id = 1
        calculate_repayment_schedule(loan_id)

        self.assertEqual(mock_connect.call_count, 1)

    @patch('your_module.engine.connect')
    def test_loan_not_found(self, mock_connect):
        mock_connect.return_value.execute.return_value.fetchall.return_value = None
        mock_connect.return_value.close.return_value = None

        loan_id = 1
        calculate_repayment_schedule(loan_id)

        self.assertEqual(mock_connect.call_count, 1)
        self.assertIn(f"No loan found for ID {loan_id}", caplog.text)

    @patch('your_module.engine.connect')
    def test_invalid_loan_id(self, mock_connect):
        loan_id = 'not_an_integer'
        with self.assertRaises(TypeError):
            calculate_repayment_schedule(loan_id)

    @patch('your_module.engine.connect')
    def test_multiplication_by_zero(self, mock_connect):
        mock_connect.return_value.execute.return_value.fetchall.return_value = (
            (0, 5, 60, '2022-01-01'),
        )
        loan_id = 1
        calculate_repayment_schedule(loan_id)

    @patch('your_module.engine.connect')
    def test_non_numeric_interest_rate(self, mock_connect):
        mock_connect.return_value.execute.return_value.fetchall.return_value = (
            (1000, 'non numeric', 60, '2022-01-01'),
        )
        loan_id = 1
        with self.assertRaises(TypeError):
            calculate_repayment_schedule(loan_id)

    @patch('your_module.engine.connect')
    def test_non_numeric_loan_term(self, mock_connect):
        mock_connect.return_value.execute.return_value.fetchall.return_value = (
            (1000, 5, 'non numeric', '2022-01-01'),
        )
        loan_id = 1
        with self.assertRaises(TypeError):
            calculate_repayment_schedule(loan_id)

    @patch('your_module.engine.connect')
    def test_loanterm_is_zero(self, mock_connect):
        mock_connect.return_value.execute.return_value.fetchall.return_value = (
            (1000, 5, 0, '2022-01-01'),
        )
        loan_id = 1
        with self.assertRaises(ZeroDivisionError):
            calculate_repayment_schedule(loan_id)

    @patch('your_module.engine.connect')
    def test_short_circuit(self, mock_connect):
        mock_connect.return_value.execute.return_value.fetchall.return_value = None
        loan_id = 1
        calculate_repayment_schedule(loan_id)
        self.assertEqual(mock_connect.call_count, 1)

if __name__ == '__main__':
    unittest.main()
