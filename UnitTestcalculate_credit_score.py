
import unittest
from unittest.mock import patch, mock_sqlalchemy
from your_file import calculate_credit_score

class TestCalculateCreditScore(unittest.TestCase):

    @patch('config.engine')
    @patch('sqlalchemy.text')
    def test_calculate_credit_score_valid_input(self, mock_text, mock_engine):
        p_customer_id = 1
        mock_engine.execute.text.return_value = [(100,)]
        mock_engine.execute.return_value = [(50,)]
        mock_engine.execute.text.return_value = [(50,)]
        mock_engine.execute.return_value = [(1,)]
        mock_engine.execute.text.return_value = [(5000,)]

        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 600)

    @patch('config.engine')
    @patch('sqlalchemy.text')
    def test_calculate_credit_score_zero_loan_amount(self, mock_text, mock_engine):
        p_customer_id = 1
        mock_engine.execute.text.return_value = [(0,)]
        mock_engine.execute.return_value = [(50,)]
        mock_engine.execute.text.return_value = [(50,)]
        mock_engine.execute.return_value = [(1,)]
        mock_engine.execute.text.return_value = [(5000,)]

        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 550)

    @patch('config.engine')
    @patch('sqlalchemy.text')
    def test_calculate_credit_score_no_credit_card(self, mock_text, mock_engine):
        p_customer_id = 1
        mock_engine.execute.text.return_value = [(100,)]
        mock_engine.execute.return_value = [(50,)]
        mock_engine.execute.text.return_value = [(50,)]
        mock_engine.execute.return_value = [(0,)]
        mock_engine.execute.text.return_value = [(0,)]

        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 550)

    @patch('config.engine')
    @patch('sqlalchemy.text')
    def test_calculate_credit_score_late_payments(self, mock_text, mock_engine):
        p_customer_id = 1
        mock_engine.execute.text.return_value = [(100,)]
        mock_engine.execute.return_value = [(50,)]
        mock_engine.execute.text.return_value = [(50,)]
        mock_engine.execute.return_value = [(1,)]
        mock_engine.execute.text.return_value = [(5000,)]
        mock_engine.execute.text.return_value = [(2,)]

        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 500)

    @patch('config.engine')
    @patch('sqlalchemy.text')
    def test_calculate_credit_score_very_low_score(self, mock_text, mock_engine):
        p_customer_id = 1
        mock_engine.execute.text.return_value = [(100,)]
        mock_engine.execute.return_value = [(50,)]
        mock_engine.execute.text.return_value = [(50,)]
        mock_engine.execute.return_value = [(1,)]
        mock_engine.execute.text.return_value = [(1000,)]
        mock_engine.execute.text.return_value = [(3,)]

        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 550)

    @patch('config.engine')
    @patch('sqlalchemy.text')
    def test_calculate_credit_score_update_customer_and_log_alert(self, mock_text, mock_engine):
        p_customer_id = 1
        mock_engine.execute.text.return_value = [(100,)]
        mock_engine.execute.return_value = [(50,)]
        mock_engine.execute.text.return_value = [(50,)]
        mock_engine.execute.return_value = [(1,)]
        mock_engine.execute.text.return_value = [(1000,)]

        result = calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(text("UPDATE customers SET credit_score = ROUND(:v_credit_score, 0) WHERE id = :p_customer_id"), v_credit_score=550, p_customer_id=p_customer_id)
        mock_engine.execute.assert_called_once_with(text("INSERT INTO credit_score_alerts (customer_id, credit_score, created_at) VALUES (:p_customer_id, ROUND(:v_credit_score, 0), NOW())"), p_customer_id=p_customer_id, v_credit_score=550)

    def test_calculate_credit_score_invalid_input(self):
        p_customer_id = 'test'
        with self.assertRaises(ValueError):
            calculate_credit_score(p_customer_id)

if __name__ == '__main__':
    unittest.main()
