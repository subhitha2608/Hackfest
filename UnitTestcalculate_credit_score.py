
import unittest
from unittest.mock import patch, MagicMock
from your_module import calculate_credit_score  # Replace with the actual module name

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_credit_score_happy_path(self, mock_engine):
        mock_engine.execute.return_value = [
            (10000.0, 8000.0, 2000.0),  # total loan amount, total repayment, outstanding balance
            (500.0,),  # credit card balance
            (2,)  # late payment count
        ]
        mock_engine.raw_connection.return_value = MagicMock-commit()

        result = calculate_credit_score(1)
        self.assertEqual(result, 700)

    @patch('your_module.engine')
    def test_calculate_credit_score_zero_loan_amount(self, mock_engine):
        mock_engine.execute.return_value = [
            (0.0, 0.0, 0.0),  # total loan amount, total repayment, outstanding balance
            (500.0,),  # credit card balance
            (2,)  # late payment count
        ]
        mock_engine.raw_connection.return_value = MagicMock-commit()

        result = calculate_credit_score(1)
        self.assertEqual(result, 650)

    @patch('your_module.engine')
    def test_calculate_credit_score_zero_credit_card_balance(self, mock_engine):
        mock_engine.execute.return_value = [
            (10000.0, 8000.0, 2000.0),  # total loan amount, total repayment, outstanding balance
            (0.0,),  # credit card balance
            (2,)  # late payment count
        ]
        mock_engine.raw_connection.return_value = MagicMock-commit()

        result = calculate_credit_score(1)
        self.assertEqual(result, 700)

    @patch('your_module.engine')
    def test_calculate_credit_score_zero_late_payments(self, mock_engine):
        mock_engine.execute.return_value = [
            (10000.0, 8000.0, 2000.0),  # total loan amount, total repayment, outstanding balance
            (500.0,),  # credit card balance
            (0,)  # late payment count
        ]
        mock_engine.raw_connection.return_value = MagicMock-commit()

        result = calculate_credit_score(1)
        self.assertEqual(result, 750)

    @patch('your_module.engine')
    def test_calculate_credit_score_low_credit_score(self, mock_engine):
        mock_engine.execute.return_value = [
            (10000.0, 8000.0, 2000.0),  # total loan amount, total repayment, outstanding balance
            (9000.0,),  # credit card balance
            (5,)  # late payment count
        ]
        mock_engine.raw_connection.return_value = MagicMock-commit()

        result = calculate_credit_score(1)
        self.assertEqual(result, 300)

    @patch('your_module.engine')
    def test_calculate_credit_score_high_credit_score(self, mock_engine):
        mock_engine.execute.return_value = [
            (0.0, 0.0, 0.0),  # total loan amount, total repayment, outstanding balance
            (0.0,),  # credit card balance
            (0,)  # late payment count
        ]
        mock_engine.raw_connection.return_value = MagicMock-commit()

        result = calculate_credit_score(1)
        self.assertEqual(result, 850)

if __name__ == '__main__':
    unittest.main()
