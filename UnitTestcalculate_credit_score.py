
import unittest
from unittest.mock import patch, Mock
from credit_score_calculator import credit_score_calculator

class TestCreditScoreCalculator(unittest.TestCase):
    @patch('credit_score_calculator.engine.connect')
    @patch('credit_score_calculator.text')
    def test_calculate_credit_score(self, mock_text, mock_connect):
        mock_connect.return_value = Mock()
        mock_query.return_value = Mock()
        mock_query.fetchone.return_value = (100, 50, 20)
        mock_query2.return_value = Mock()
        mock_query2.fetchone.return_value = (10)
        mock_query3.return_value = Mock()
        mock_query3.fetchone.return_value = (1)

        result = credit_score_calculator(1)

        self.assertEqual(result, 550)

    @patch('credit_score_calculator.engine.connect')
    @patch('credit_score_calculator.text')
    def test_calculate_credit_score_zero_total_loan_amount(self, mock_text, mock_connect):
        mock_connect.return_value = Mock()
        mock_query.return_value = Mock()
        mock_query.fetchone.return_value = (0, 0, 0)
        mock_query2.return_value = Mock()
        mock_query2.fetchone.return_value = (0)
        mock_query3.return_value = Mock()
        mock_query3.fetchone.return_value = (0)

        result = credit_score_calculator(1)

        self.assertEqual(result, 700)

    @patch('credit_score_calculator.engine.connect')
    @patch('credit_score_calculator.text')
    def test_calculate_credit_score_low_credit_card_balance(self, mock_text, mock_connect):
        mock_connect.return_value = Mock()
        mock_query.return_value = Mock()
        mock_query.fetchone.return_value = (100, 50, 20)
        mock_query2.return_value = Mock()
        mock_query2.fetchone.return_value = (0)
        mock_query3.return_value = Mock()
        mock_query3.fetchone.return_value = (1)

        result = credit_score_calculator(1)

        self.assertEqual(result, 650)

    @patch('credit_score_calculator.engine.connect')
    @patch('credit_score_calculator.text')
    def test_calculate_credit_score_high_late_pay_count(self, mock_text, mock_connect):
        mock_connect.return_value = Mock()
        mock_query.return_value = Mock()
        mock_query.fetchone.return_value = (100, 50, 20)
        mock_query2.return_value = Mock()
        mock_query2.fetchone.return_value = (10)
        mock_query3.return_value = Mock()
        mock_query3.fetchone.return_value = (5)

        result = credit_score_calculator(1)

        self.assertEqual(result, 420)

    @patch('credit_score_calculator.engine.connect')
    @patch('credit_score_calculator.text')
    def test_calculate_credit_score_update_credit_score_database(self, mock_text, mock_connect):
        mock_connect.return_value = Mock()
        mock_query.return_value = Mock()
        mock_query.fetchone.return_value = (100, 50, 20)
        mock_query2.return_value = Mock()
        mock_query2.fetchone.return_value = (10)
        mock_query3.return_value = Mock()
        mock_query3.fetchone.return_value = (1)

        credit_score_calculator(1)

        mock_query4.return_value = Mock()
        mock_query4.execute.called_once_with({'p_customer_id': 1, 'v_credit_score': 420})

    @patch('credit_score_calculator.engine.connect')
    @patch('credit_score_calculator.text')
    def test_calculate_credit_score_log_result_low_score(self, mock_text, mock_connect):
        mock_connect.return_value = Mock()
        mock_query.return_value = Mock()
        mock_query.fetchone.return_value = (100, 50, 20)
        mock_query2.return_value = Mock()
        mock_query2.fetchone.return_value = (10)
        mock_query3.return_value = Mock()
        mock_query3.fetchone.return_value = (1)

        credit_score_calculator(1)

        mock_query5.return_value = Mock()
        mock_query5.execute.called_once_with({'p_customer_id': 1, 'v_credit_score': 420})

if __name__ == '__main__':
    unittest.main()
