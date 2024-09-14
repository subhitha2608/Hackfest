
import unittest
from unittest.mock import patch, Mock
from your_module import calculate_credit_score  # import the function to test

class TestCalculateCreditScore(unittest.TestCase):
    @patch('your_module.engine')
    def test_calculate_credit_score(self, mock_engine):
        # Test case 1: valid customer id, no loans
        p_customer_id = 123
        mock_engine.execute.return_value.fetchall.return_value = [(0, 0, 0)]  # total loan amount, total repayment, outstanding balance
        mock_engine.execute.return_value.fetchall.return_value = [1000.0]  # credit card balance
        mock_engine.execute.return_value.fetchall.return_value = [0]  # late pay count
        credit_score = calculate_credit_score(p_customer_id)
        self.assertEqual(credit_score, 550.0)

        # Test case 2: valid customer id, with loans
        p_customer_id = 456
        mock_engine.execute.return_value.fetchall.return_value = [(1000.0, 500.0, 200.0)]  # total loan amount, total repayment, outstanding balance
        mock_engine.execute.return_value.fetchall.return_value = [500.0]  # credit card balance
        mock_engine.execute.return_value.fetchall.return_value = [1]  # late pay count
        credit_score = calculate_credit_score(p_customer_id)
        self.assertEqual(credit_score, 800.0)

        # Test case 3: invalid customer id
        p_customer_id = 789
        with self.assertRaises(Exception):
            calculate_credit_score(p_customer_id)

        # Test case 4: no rows returned from database
        p_customer_id = 123
        mock_engine.execute.return_value.fetchall.return_value = []
        with self.assertRaises(Exception):
            calculate_credit_score(p_customer_id)

        # Test case 5: update customer credit score
        p_customer_id = 123
        credit_score = calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(text("""
            UPDATE customers
            SET credit_score = ROUND(:credit_score, 0)
            WHERE customers.id = :p_customer_id
        """), p_customer_id=p_customer_id, credit_score=credit_score)

    @patch('your_module.engine')
    def test_log_credit_score_alert(self, mock_engine):
        p_customer_id = 123
        credit_score = 400
        mock_engine.execute.return_value.fetchall.return_value = []  # dummy result
        calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(text("""
            INSERT INTO credit_score_alerts (customer_id, credit_score, created_at)
            VALUES (:p_customer_id, ROUND(:credit_score, 0), NOW())
        """), p_customer_id=p_customer_id, credit_score=credit_score)

if __name__ == '__main__':
    unittest.main()
