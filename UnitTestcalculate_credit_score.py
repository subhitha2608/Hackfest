
import unittest
from credit_score import calculate_credit_score
from unittest.mock import patch, Mock

class TestCalculateCreditScore(unittest.TestCase):
    @patch('config.engine')
    @patch('config.text')
    def test_calculate_credit_score(
        self, mock_text, mock_engine
    ):
        # Setup
        p_customer_id = 123
        mock_engine.execute.return_value = Mock(fetchone=lambda: (100, 200, 300))
        mock_text.return_value = 'SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), COALESCE(ROUND(SUM(repayment_amount), 2), 0), COALESCE(ROUND(SUM(outstanding_balance), 2), 0)'

        # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 700)

        # Step 2: Get the current credit card balance
        mock_engine.execute.return_value = Mock(fetchone=lambda: (400,))
        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 650)

        # Step 3: Count the number of late payments
        mock_engine.execute.return_value = Mock(fetchone=lambda: (1,))
        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 600)

        # Step 4: Basic rule-based calculation of the credit score
        mock_engine.execute.return_value = Mock(fetchone=lambda: (0,))
        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 400)

        # Step 5: Update the customer’s credit score in the database
        mock_engine.execute.return_value = Mock()
        calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(
            query=mock.ANY, p_customer_id=p_customer_id, v_credit_score=700
        )

        # Optionally, log the result or raise an alert for very low scores
        mock_engine.execute.return_value = Mock()
        calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(
            query=mock.ANY, p_customer_id=p_customer_id, v_credit_score=400
        )

    def test_low_credit_score(self):
        # Setup
        p_customer_id = 123
        mock_engine.execute.return_value = Mock(fetchone=lambda: (0,))
        mock_text.return_value = 'SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), COALESCE(ROUND(SUM(repayment_amount), 2), 0), COALESCE(ROUND(SUM(outstanding_balance), 2), 0)'

        # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 400)

        # Step 5: Update the customer’s credit score in the database
        mock_engine.execute.return_value = Mock()
        calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(
            query=mock.ANY, p_customer_id=p_customer_id, v_credit_score=400
        )

        # Optionally, log the result or raise an alert for very low scores
        mock_engine.execute.return_value = Mock()
        calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(
            query=mock.ANY, p_customer_id=p_customer_id, v_credit_score=400
        )

    def test_high_credit_score(self):
        # Setup
        p_customer_id = 123
        mock_engine.execute.return_value = Mock(fetchone=lambda: (1000, 2000, 3000))
        mock_text.return_value = 'SELECT COALESCE(ROUND(SUM(loan_amount), 2), 0), COALESCE(ROUND(SUM(repayment_amount), 2), 0), COALESCE(ROUND(SUM(outstanding_balance), 2), 0)'

        # Step 1: Calculate the customer's total loan amount, total repayment, and outstanding balance
        result = calculate_credit_score(p_customer_id)
        self.assertEqual(result, 850)

        # Step 5: Update the customer’s credit score in the database
        mock_engine.execute.return_value = Mock()
        calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(
            query=mock.ANY, p_customer_id=p_customer_id, v_credit_score=850
        )

        # Optionally, log the result or raise an alert for very low scores
        mock_engine.execute.return_value = Mock()
        calculate_credit_score(p_customer_id)
        mock_engine.execute.assert_called_once_with(
            query=mock.ANY, p_customer_id=p_customer_id, v_credit_score=850
        )

if __name__ == '__main__':
    unittest.main()
